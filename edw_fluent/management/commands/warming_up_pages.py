import json
import random
import time

from django.core.cache import cache

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _, ugettext

from edw_fluent.models.page import get_simple_page_url_buffer, SimplePage
from edw_fluent.utils import get_warming_up_result
from edw_fluent.settings import DOMAIN_WITH_PROTOCOL


CACHE_LIFETIME = 3600
CACHE_KEY = 'WARMING_UP_PAGES_LIST'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--main_page',
            action='store_true',
            dest='main_page',
            default=False,
            help='warm up main page only',
        )

    @staticmethod
    def get_pages():
        qs = SimplePage.objects.filter(warm_up=True)
        return [{'pk': page.pk, 'urn': str(page.urlnode_ptr)} for page in qs]

    def cache_pages_list(self):
        cache.set(CACHE_KEY, self.get_pages(), CACHE_LIFETIME)

    def get_url_list_from_urn_list(self, urn_list):
        return [DOMAIN_WITH_PROTOCOL + page['urn'] for page in self.cached_pages if page['urn'] in urn_list]

    @property
    def cached_pages(self):
        cache_set = cache.get(CACHE_KEY, None)

        if cache_set is None:
            self.cache_pages_list()
            cache_set = cache.get(CACHE_KEY, None)

        return cache_set

    def handle(self, **options):
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