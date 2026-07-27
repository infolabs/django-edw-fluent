"""Прогрев кеша статических страниц ``SimplePage`` (management-команда ``warming_up_pages``).

Назначение
==========
Команда поддерживает "тёплым" page-кеш статических страниц, у которых включён
флаг ``warm_up=True``. За один запуск прогревается **ровно одна** ещё не
закешированная страница (либо главная страница в специальном режиме), поэтому
команда рассчитана на частый периодический запуск (например, celery-задачей
``async_warming_up_pages`` раз в минуту): постепенно, запуск за запуском, она
наполняет кеш всех отмеченных страниц.

Алгоритм работы
===============
1. **Список кандидатов.** Из БД берутся все ``SimplePage`` с ``warm_up=True`` и
   в виде списка словарей ``{'pk', 'urn'}`` кладутся в кеш под ключом
   ``WARMING_UP_PAGES_LIST`` на ``CACHE_LIFETIME`` секунд (см. свойство
   :pyattr:`Command.cached_pages` / :pymeth:`Command.cache_pages_list`).
   Это избавляет от повторных запросов к БД при частых запусках.
2. **Уже закешированные страницы.** Из кольцевого буфера
   ``get_simple_page_url_buffer()`` читается список URN уже закешированных
   страниц (``buf_urn_list``); буфер наполняется монки-патчем
   ``learn_cache_key`` при реальном кешировании ответов. Список конвертируется
   в абсолютные URL (``buf_url_list``) для вывода в отчёте.
3. **Выбор режима.**
   - ``--main_page`` — прогревается только главная страница (``urn == '/'``).
   - без флага — кандидаты перемешиваются (``random.sample``), чтобы при
     параллельных/частых запусках прогревались разные страницы.
4. **Поиск цели и прогрев.** Перебираются страницы из выборки; берётся первая,
   которой ещё нет в буфере закешированных (или главная в режиме
   ``--main_page``). Для неё вызывается ``get_warming_up_result(urn)``, который
   делает реальный HTTP-запрос через команду ``warming_up`` и наполняет кеш.
   Результат печатается в stdout как JSON, после чего команда завершается
   (**один прогрев за запуск**).
5. **Нечего прогревать.** Если подходящих страниц не осталось — выводится
   ``{"result": "all pages already cached", ...}``.

Вывод
=====
Во всех ветках печатается JSON в ``stdout`` — его разбирает вызывающая
celery-задача.

См. также
=========
``[warming_up_pages.md](../../docs/warming_up/warming_up_pages.md)`` — подробное
описание команды.
"""
import json
import random

from django.core.cache import cache

from django.core.management import call_command
from django.core.management.base import BaseCommand

from edw_fluent.models.page import get_simple_page_url_buffer, SimplePage
from edw_fluent.utils import get_warming_up_result
from edw_fluent.settings import DOMAIN_WITH_PROTOCOL


CACHE_LIFETIME = 3600
CACHE_KEY = 'WARMING_UP_PAGES_LIST'


class Command(BaseCommand):
    """Прогрев page-кеша статических страниц ``SimplePage`` с ``warm_up=True``.

    За один запуск прогревает одну ещё не закешированную страницу (или главную
    в режиме ``--main_page``). Список страниц-кандидатов кешируется под ключом
    ``CACHE_KEY`` на ``CACHE_LIFETIME`` секунд. Подробный алгоритм — в docstring
    модуля.
    """

    def add_arguments(self, parser):
        """Регистрирует аргументы командной строки.

        Args:
            parser (argparse.ArgumentParser): парсер аргументов команды.

        Побочные эффекты:
            Добавляет флаг ``--main_page`` (``dest='main_page'``,
            ``action='store_true'``, по умолчанию ``False``) — при его наличии
            прогревается только главная страница (``urn == '/'``).

        Returns:
            None
        """
        parser.add_argument(
            '--main_page',
            action='store_true',
            dest='main_page',
            default=False,
            help='warm up main page only',
        )

    @staticmethod
    def get_pages():
        """Возвращает страницы-кандидаты для прогрева напрямую из БД.

        Выбирает все ``SimplePage`` с ``warm_up=True`` и приводит их к
        сериализуемому виду, пригодному для хранения в кеше.

        Args:
            Нет.

        Returns:
            list[dict]: список словарей ``{'pk': int, 'urn': str}``, где
            ``urn`` — строковое представление ``page.urlnode_ptr`` (путь
            страницы).
        """
        qs = SimplePage.objects.filter(warm_up=True)
        return [{'pk': page.pk, 'urn': str(page.urlnode_ptr)} for page in qs]

    def cache_pages_list(self):
        """Складывает список страниц-кандидатов в кеш.

        Вызывает :pymeth:`get_pages` и сохраняет результат под ключом
        ``CACHE_KEY`` со сроком жизни ``CACHE_LIFETIME`` секунд.

        Args:
            Нет.

        Returns:
            None

        Побочные эффекты:
            Запись в кеш по ключу ``CACHE_KEY``.
        """
        cache.set(CACHE_KEY, self.get_pages(), CACHE_LIFETIME)

    def get_url_list_from_urn_list(self, urn_list):
        """Преобразует список URN в абсолютные URL закешированных страниц.

        Оставляет только те страницы из :pyattr:`cached_pages`, чьи ``urn``
        присутствуют в ``urn_list``, и приклеивает к ним домен с протоколом.

        Args:
            urn_list (Iterable[str]): список/множество URN (путей) уже
                закешированных страниц (обычно из кольцевого буфера).

        Returns:
            list[str]: абсолютные URL вида ``DOMAIN_WITH_PROTOCOL + urn`` для
            страниц-кандидатов, попавших в ``urn_list``.
        """
        return [DOMAIN_WITH_PROTOCOL + page['urn'] for page in self.cached_pages if page['urn'] in urn_list]

    @property
    def cached_pages(self):
        """Список страниц-кандидатов с ленивым наполнением кеша.

        Читает список из кеша по ключу ``CACHE_KEY``; при промахе наполняет его
        через :pymeth:`cache_pages_list` и перечитывает.

        Args:
            Нет.

        Returns:
            list[dict]: список словарей ``{'pk': int, 'urn': str}`` страниц с
            ``warm_up=True``.
        """
        cache_set = cache.get(CACHE_KEY, None)

        if cache_set is None:
            self.cache_pages_list()
            cache_set = cache.get(CACHE_KEY, None)

        return cache_set

    def handle(self, **options):
        """Точка входа команды: прогревает одну страницу и печатает JSON-отчёт.

        Порядок действий:

        1. Читает из кольцевого буфера ``get_simple_page_url_buffer()`` список
           URN уже закешированных страниц и формирует их абсолютные URL.
        2. В зависимости от флага ``--main_page`` выбирает либо только главную
           страницу (``urn == '/'``), либо все кандидаты в случайном порядке.
        3. Находит первую страницу, которой ещё нет в буфере закешированных
           (или главную в режиме ``--main_page``), прогревает её через
           ``get_warming_up_result`` и печатает результат.
        4. Если прогревать нечего — печатает отчёт ``all pages already cached``.

        Args:
            **options: опции команды; используется ``main_page`` (bool) —
                режим прогрева только главной страницы.

        Returns:
            None

        Побочные эффекты:
            HTTP-запрос к странице (через ``get_warming_up_result`` →
            команда ``warming_up``), наполнение page-кеша и запись
            JSON-отчёта в ``self.stdout``.
        """
        buf = get_simple_page_url_buffer()
        buf_urn_list = buf.get_all()
        buf_url_list = self.get_url_list_from_urn_list(buf_urn_list)

        only_main_page = options.get('main_page')

        qs = self.cached_pages
        if only_main_page:
            shuffled_qs = [page for page in qs if page['urn'] == '/']
        else:
            shuffled_qs = random.sample(qs, k=len(qs))

        for page in shuffled_qs:
            if page['urn'] not in buf_urn_list or only_main_page:
                result = {'pk': page['pk']}

                result.update(get_warming_up_result(page['urn']))
                result.update({'cached_pages': buf_url_list})
                if only_main_page:
                    result.update({"detail": "warming up main page after publication post save"})
                self.stdout.write(json.dumps(result))
                return

        self.stdout.write(json.dumps({"result": "all pages already cached", "cached pages": buf_url_list}))