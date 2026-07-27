---
name: Кеширование страниц SimplePage
overview: "Механизм page-кеша статических страниц SimplePage (django-edw-fluent): декоратор cache_simple_page на SimplePagePlugin.get_response, SimplePageCacheMiddleware, монки-патч learn_cache_key, первичный и вторичный слои кеша, кольцевые буферы (ключей, URL, secondary), инвалидация через сигналы и прогрев командой warming_up_pages."
---

# Кеширование страниц `SimplePage`

Документ описывает, как кешируются статические страницы `SimplePage`
(тип страницы `django-fluent-pages`) в пакете `django-edw-fluent`.

Основной код: `[../../models/page.py](../../models/page.py)`.

## Обзор

Ответ страницы `SimplePage` кешируется целиком (полный HTML) на уровне
рендеринга страницы плагином `fluent_pages`. Кеш строится поверх стандартного
Django page-cache (`CacheMiddleware`), но с тремя доработками:

1. **Реестр ключей в кольцевом буфере** — чтобы можно было массово
   инвалидировать все закешированные страницы.
2. **Вторичный слой кеша** (`sspb:*`) — fallback-копия ответа для
   ре-гидрации первичного слоя (anti-stampede / stale-while-revalidate).
3. **Буфер URL** — список путей уже закешированных страниц (используется
   прогревом `warming_up_pages`).

Кешируются ответы **только для анонимных пользователей** и только со статусом
`200`/`304`.

## Точка подключения

Кеш включается декоратором `cache_simple_page` на методе рендера плагина
страницы:

```74:79:edw_fluent/admin/page.py
    @method_decorator(cache_simple_page(getattr(settings, 'SIMPLE_PAGE_CACHE_TIMEOUT', 60*10)))
    def get_response(self, request, page, **kwargs):
        """
        RUS: Генерирует вывод страницы.
        """
        return super(SimplePagePlugin, self).get_response(request, page, **kwargs)
```

`cache_simple_page(timeout)` — обёртка над `SimplePageCacheMiddleware` через
`decorator_from_middleware_with_args`, то есть кеш применяется точечно к
рендеру `SimplePage`, а не глобально ко всем запросам.

## Константы и настройки

Определены в `[../../models/page.py](../../models/page.py)`:

| Константа | Значение / настройка | Назначение |
|---|---|---|
| `SIMPLE_PAGE_BUFFER_CACHE_KEY` | `'spg_bf'` | Ключ кольцевого буфера первичных `cache_key`. |
| `SIMPLE_PAGE_BUFFER_CACHE_SIZE` | `SIMPLE_PAGE_BUFFER_CACHE_SIZE` (по умолч. 100) | Ёмкость буфера ключей. |
| `SIMPLE_PAGE_URL_BUFFER_CACHE_KEY` | `'spg_url_bf'` | Ключ буфера URL закешированных страниц. |
| `SIMPLE_PAGE_URL_BUFFER_CACHE_SIZE` | `100` | Ёмкость буфера URL. |
| `SIMPLE_PAGE_URL_CACHE_TIMEOUT` | `SIMPLE_PAGE_CACHE_TIMEOUT` (по умолч. 3600) | TTL буфера URL. |
| `SECONDARY_SIMPLE_PAGE_BUFFER_CACHE_KEY` | `'sec_spg_bf'` | Ключ кольцевого буфера вторичных ключей. |
| `SECONDARY_SIMPLE_PAGE_BUFFER_CACHE_KEY_PATTERN` | `'sspb:{key}'` | Паттерн ключа вторичной копии ответа. |
| `SECONDARY_SIMPLE_PAGE_BUFFER_CACHE_TIMEOUT` | `SECONDARY_SIMPLE_PAGE_BUFFER_CACHE_TIMEOUT` (по умолч. 86400) | TTL вторичной копии (1 день). |
| таймаут декоратора | `SIMPLE_PAGE_CACHE_TIMEOUT` (по умолч. 600) | TTL первичного page-кеша. |

Кольцевые буферы реализованы классом `RingBuffer`
(`[edw/utils/circular_buffer_in_cache.py](edw/utils/circular_buffer_in_cache.py)`,
пакет `django-edw`): хранит фиксированное число элементов в кеше, при
переполнении вытесняет самый старый (FIFO).

## Слои кеша

| Слой | Ключ | Что хранит | TTL |
|---|---|---|---|
| Первичный page-кеш | Django `cache_key` (из `learn_cache_key`) | Отрендеренный `HttpResponse` страницы | `SIMPLE_PAGE_CACHE_TIMEOUT` |
| Реестр ключей | буфер `spg_bf` | Список первичных `cache_key` (для вытеснения/инвалидации) | 30 дней (буфер) |
| Буфер URL | буфер `spg_url_bf` | `request.path` закешированных страниц | `SIMPLE_PAGE_URL_CACHE_TIMEOUT` |
| Вторичный слой | `sspb:{cache_key}` | Копия ответа для ре-гидрации | `SECONDARY_SIMPLE_PAGE_BUFFER_CACHE_TIMEOUT` |
| Реестр вторичных ключей | буфер `sec_spg_bf` | Список ключей `sspb:*` | 30 дней (буфер) |

## Поток запроса

```mermaid
flowchart TD
    A[GET страница SimplePage] --> B{Пользователь\nаутентифицирован?}
    B -->|да| Z[Кеш пропускается,\nобычный рендер]
    B -->|нет| C[process_request:\nстандартный page-cache lookup]
    C --> D{Первичный\ncache_key есть?}
    D -->|да| E[Отдать ответ из кеша]
    D -->|нет| F{Есть вторичная\nкопия sspb:cache_key?}
    F -->|да| G[Ре-гидрация:\ncache.set primary = secondary,\nответ отдаст следующий шаг]
    F -->|нет| H[Рендер во вью\n(get_response)]
    H --> I[process_response:\nкеширование ответа]
```

### `process_request` (чтение)

`SimplePageCacheMiddleware.process_request`
(`[../../models/page.py](../../models/page.py)`):

1. Для аутентифицированных — `None` (кеш не используется).
2. Иначе вызывает стандартный `CacheMiddleware.process_request` (первичный
   lookup).
3. Если первичного ответа нет — пытается достать вторичную копию
   `sspb:{cache_key}` и, если она есть, кладёт её в первичный слой (ре-гидрация),
   чтобы конкурентные запросы получили ответ, пока идёт свежий рендер.

### `process_response` (запись)

`SimplePageCacheMiddleware.process_response`:

1. Пропускает кеширование для аутентифицированных, стриминга, статусов кроме
   `200`/`304`, ответов с user-specific cookie и `max-age=0`.
2. Определяет `timeout` (из `Cache-Control: max-age` или дефолтный).
3. Вычисляет `cache_key` через монки-патченный `learn_cache_key` (см. ниже).
4. Для рендеримых ответов вешает `post_render_callback`, который:
   - пишет отрендеренный ответ в **первичный** слой (`cache_key`);
   - пишет копию во **вторичный** слой (`sspb:{cache_key}`), регистрируя ключ
     в кольцевом буфере `sec_spg_bf` и вытесняя старый.

### Монки-патч `learn_cache_key`

Функция `learn_cache_key` (`[../../models/page.py](../../models/page.py)`)
поверх стандартного `django.utils.cache.learn_cache_key`:

1. Вычисляет и возвращает первичный `cache_key`.
2. Регистрирует `cache_key` в кольцевом буфере `spg_bf`; при переполнении
   удаляет вытесненный старый ключ из кеша.
3. Дополнительно кладёт `request.path` в буфер URL `spg_url_bf` (для прогрева),
   так же вытесняя старый.

## Инвалидация

Инвалидация массовая: очищаются кольцевые буферы, а зарегистрированные в них
ключи удаляются из кеша.

| Функция | Что делает |
|---|---|
| `clear_simple_page_buffer()` | Берёт все ключи из буфера `spg_bf`, очищает буфер и удаляет ключи из кеша (`delete_many`). |
| `clear_simple_page_url_buffer()` | То же для буфера URL `spg_url_bf`. |

Вызовы (сигналы, `[../../signals/handlers/](../../signals/handlers/)`):

| Обработчик | Сигнал / sender | Действие |
|---|---|---|
| `invalidate_simple_page_after_save` / `..._before_delete` | `post_save` / `pre_delete` `SimplePage` (`[../../signals/handlers/simple_page.py](../../signals/handlers/simple_page.py)`) | `clear_simple_page_buffer()` + `clear_simple_page_url_buffer()` |
| `invalidate_entity_after_save` / `..._before_delete` | `post_save` / `pre_delete` Entity и всех подклассов, включая `Publication` (`[../../signals/handlers/entity.py](../../signals/handlers/entity.py)`) | `clear_simple_page_buffer()` |
| `invalidate_data_mart_after_save` / `..._before_delete` | `post_save` / `pre_delete` DataMart (`[../../signals/handlers/data_mart.py](../../signals/handlers/data_mart.py)`) | `clear_simple_page_buffer()` |
| `invalidate_term_after_save` / `..._before_delete` / `..._after_move` | `post_save` / `pre_delete` / `move_to_done` Term (`[../../signals/handlers/term.py](../../signals/handlers/term.py)`) | `clear_simple_page_buffer()` |

То есть любая правка страницы, сущности (в т.ч. публикации в **любом**
статусе), витрины или термина сбрасывает первичный page-кеш всех `SimplePage`.
Вторичный слой (`sspb:*`) при этом **не** очищается — из него возможна
ре-гидрация до следующего рендера. Обратите внимание: сохранение Entity
чистит только первичный буфер (`clear_simple_page_buffer`), но **не** буфер URL
(`spg_url_bf`) — его чистит лишь сигнал `SimplePage`.

## Прогрев

Пустой после инвалидации кеш наполняется командой `warming_up_pages`
(реальный HTTP-запрос к странице). Подробно —
`[../warming_up/warming_up_pages.md](../warming_up/warming_up_pages.md)`.
Команда использует буфер URL (`get_simple_page_url_buffer`), чтобы прогревать
только ещё не закешированные страницы, и флаг `SimplePage.warm_up`.

## Модель `SimplePage`

`SimplePage` (`[../../models/page.py](../../models/page.py)`) — тип страницы
`fluent_pages` (`AbstractFluentPage`). Поля, значимые для кеша/прогрева:

- `warm_up` (bool) — включает периодический прогрев страницы;
- `terms` (M2M `Term`), `seo_title` — влияют на контекст рендера.

## Справочник функций

| Функция / класс | Файл | Назначение |
|---|---|---|
| `get_simple_page_buffer()` | `../../models/page.py` | Кольцевой буфер первичных `cache_key`. |
| `get_simple_page_url_buffer()` | `../../models/page.py` | Кольцевой буфер URL закешированных страниц. |
| `get_secondary_simple_page_buffer()` | `../../models/page.py` | Кольцевой буфер вторичных ключей `sspb:*`. |
| `clear_simple_page_buffer()` | `../../models/page.py` | Массовый сброс первичного page-кеша. |
| `clear_simple_page_url_buffer()` | `../../models/page.py` | Сброс буфера URL. |
| `learn_cache_key(request, response, timeout, key_prefix, cache)` | `../../models/page.py` | Монки-патч: вычисление `cache_key` + регистрация в буферах + вытеснение. |
| `SimplePageCacheMiddleware` | `../../models/page.py` | Middleware чтения/записи кеша с secondary-слоем. |
| `cache_simple_page(timeout, cache=None, key_prefix=None)` | `../../models/page.py` | Декоратor вью на базе middleware. |
| `RingBuffer` | `edw/utils/circular_buffer_in_cache.py` | Кольцевой буфер в кеше (FIFO-вытеснение). |
