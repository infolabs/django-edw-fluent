---
name: Прогрев кеша статических страниц
overview: "Management-команда warming_up_pages: прогрев page-кеша статических страниц SimplePage (warm_up=True). Алгоритм работы, режимы (--main_page), кеш списка кандидатов, кольцевой буфер закешированных URL, описание всех функций с входными и выходными параметрами."
---

# Команда `warming_up_pages`

Файл: `[edw_fluent/management/commands/warming_up_pages.py](../../management/commands/warming_up_pages.py)`

Management-команда прогрева (warm-up) page-кеша **статических страниц** `SimplePage`, у которых включён флаг `warm_up=True`. За один запуск прогревается **ровно одна** ещё не закешированная страница (или главная в специальном режиме), поэтому команда рассчитана на частый периодический запуск.

## Назначение

Держать «тёплым» кеш статических страниц, чтобы пользователи не попадали на холодный рендер. Список страниц для прогрева определяется флагом `warm_up` в модели `SimplePage`:

```250:254:edw_fluent/models/page.py
    warm_up = models.BooleanField(
        verbose_name=_('Do warm up'),
        default=False,
        help_text=_('If True, a request will be made to the page on a schedule to update the cache')
    )
```

Команда обычно вызывается celery-задачей `async_warming_up_pages` (`[edw_fluent/tasks/async_warming_up_pages.py](../../tasks/async_warming_up_pages.py)`), которую рекомендуется запускать по расписанию (например, раз в минуту). За счёт «один прогрев за запуск» кеш всех отмеченных страниц наполняется постепенно.

## Константы

| Константа | Значение | Назначение |
|---|---|---|
| `CACHE_KEY` | `'WARMING_UP_PAGES_LIST'` | Ключ кеша со списком страниц-кандидатов (`warm_up=True`). |
| `CACHE_LIFETIME` | `3600` | Срок жизни (сек.) списка кандидатов в кеше. |

Дополнительно используется кольцевой буфер `get_simple_page_url_buffer()` (`[edw_fluent/models/page.py](../../models/page.py)`), где хранятся URN уже закешированных страниц. Буфер наполняется монки-патчем `learn_cache_key` в момент реального кеширования ответа страницы.

## Алгоритм работы

1. **Формирование списка кандидатов.**
   Все `SimplePage` с `warm_up=True` выбираются из БД и сериализуются в список словарей `{'pk', 'urn'}`, который кладётся в кеш под ключом `CACHE_KEY` на `CACHE_LIFETIME` секунд. При последующих запусках список берётся из кеша без обращения к БД (свойство `cached_pages` + метод `cache_pages_list`).

2. **Чтение уже закешированных страниц.**
   Из кольцевого буфера `get_simple_page_url_buffer()` читается список URN уже закешированных страниц (`buf_urn_list`). Этот список конвертируется в абсолютные URL (`buf_url_list`) для отчёта.

3. **Выбор режима прогрева.**
   - С флагом `--main_page` — в выборку попадает только главная страница (`urn == '/'`).
   - Без флага — список кандидатов перемешивается (`random.sample`), чтобы при частых/параллельных запусках прогревались разные страницы.

4. **Поиск цели и прогрев.**
   Перебираются страницы выборки; берётся первая, которой ещё **нет** в буфере закешированных (`page['urn'] not in buf_urn_list`), либо главная в режиме `--main_page`. Для неё вызывается `get_warming_up_result(urn)`, который делает реальный HTTP-запрос через команду `warming_up` и наполняет кеш. Результат печатается в `stdout` в виде JSON, после чего команда **завершается** (один прогрев за запуск).

5. **Если прогревать нечего.**
   Если подходящих страниц не осталось — выводится `{"result": "all pages already cached", "cached pages": [...]}`.

### Схема

```
handle(--main_page?)
  ├─ buf = get_simple_page_url_buffer()        # уже закешированные URN
  │    └─ buf_url_list = get_url_list_from_urn_list(buf_urn_list)
  ├─ qs = cached_pages                          # кандидаты warm_up=True (из кеша)
  │    └─ (miss) cache_pages_list() → get_pages()
  ├─ main_page?  → только urn == '/'
  │  иначе       → random.sample(qs)
  └─ первая страница вне буфера / главная:
       get_warming_up_result(urn) → HTTP GET → наполнение кеша
       print(json) ; return
```

## Аргументы команды

| Аргумент | Тип | По умолчанию | Описание |
|---|---|---|---|
| `--main_page` | flag (`store_true`) | `False` | Прогревать только главную страницу (`urn == '/'`). Используется, например, после сохранения публикации. |

## Вывод (stdout)

Во всех ветках печатается JSON, который разбирает вызывающая celery-задача:

- **Прогрет обычный кандидат:**
  ```json
  {"pk": 123, "urn": "/some/page/", "elapsed_time": "0.42 sec", "errors": null, "cached_pages": ["https://.../a", "..."]}
  ```
- **Прогрета главная (`--main_page`):** тот же формат плюс
  `{"detail": "warming up main page after publication post save"}`.
- **Нечего прогревать:**
  ```json
  {"result": "all pages already cached", "cached pages": ["https://.../a", "..."]}
  ```

## Описание функций

Все методы объявлены в классе `Command`.

### `add_arguments(self, parser)`

Регистрирует аргументы командной строки.

- **Вход:** `parser` (`argparse.ArgumentParser`) — парсер аргументов команды.
- **Выход:** `None`.
- **Побочные эффекты:** добавляет флаг `--main_page` (`dest='main_page'`, `action='store_true'`, по умолчанию `False`).

### `get_pages()` (staticmethod)

Возвращает страницы-кандидаты напрямую из БД.

- **Вход:** нет.
- **Выход:** `list[dict]` — список `{'pk': int, 'urn': str}` для всех `SimplePage` с `warm_up=True`; `urn` — строковое представление `page.urlnode_ptr`.

### `cache_pages_list(self)`

Кладёт список кандидатов в кеш.

- **Вход:** нет.
- **Выход:** `None`.
- **Побочные эффекты:** `cache.set(CACHE_KEY, get_pages(), CACHE_LIFETIME)`.

### `get_url_list_from_urn_list(self, urn_list)`

Преобразует список URN в абсолютные URL закешированных страниц.

- **Вход:** `urn_list` (`Iterable[str]`) — URN (пути) уже закешированных страниц (обычно из кольцевого буфера).
- **Выход:** `list[str]` — абсолютные URL вида `DOMAIN_WITH_PROTOCOL + urn` для страниц-кандидатов, попавших в `urn_list`.

### `cached_pages` (property)

Список кандидатов с ленивым наполнением кеша.

- **Вход:** нет.
- **Выход:** `list[dict]` — `{'pk': int, 'urn': str}`. При промахе кеша наполняет его через `cache_pages_list()` и перечитывает.

### `handle(self, **options)`

Точка входа команды: прогревает одну страницу и печатает JSON-отчёт.

- **Вход:** `**options` — опции команды; используется `main_page` (`bool`).
- **Выход:** `None`.
- **Побочные эффекты:** HTTP-запрос к странице (через `get_warming_up_result` → команда `warming_up`), наполнение page-кеша, запись JSON-отчёта в `self.stdout`.

## Связанные компоненты

- `get_warming_up_result(urn)` — `[edw_fluent/utils.py](../../utils.py)`: выполняет реальный прогрев через команду `warming_up`, возвращает `{'urn', 'elapsed_time', 'errors'}`.
- `get_simple_page_url_buffer()`, `learn_cache_key` — `[edw_fluent/models/page.py](../../models/page.py)`: кольцевой буфер URL закешированных страниц и его наполнение.
- `async_warming_up_pages` — `[edw_fluent/tasks/async_warming_up_pages.py](../../tasks/async_warming_up_pages.py)`: celery-обёртка для периодического запуска команды.
- `DOMAIN_WITH_PROTOCOL` — `[edw_fluent/settings.py](../../settings.py)`: домен с протоколом для построения абсолютных URL.
