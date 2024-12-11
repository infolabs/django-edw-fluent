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
    @staticmethod
    def get_pages():
        qs = SimplePage.objects.filter(warm_up=True)
        return [{'pk': page.pk, 'urn': str(page.urlnode_ptr)} for page in qs]

    @staticmethod
    def get_url_list_from_urn_list(urn_list):
        return [DOMAIN_WITH_PROTOCOL + urn for urn in urn_list]

    def cache_pages_list(self):
        cache.set(CACHE_KEY, self.get_pages(), CACHE_LIFETIME)

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

        qs = self.cached_pages
        shuffled_qs = random.sample(qs, k=len(qs))

        start_time = time.time()
        for page in shuffled_qs:
            if page['urn'] not in buf_urn_list:
                result = {'pk': page['pk']}

                result.update(get_warming_up_result(page['urn']))
                result.update({'cached_pages': buf_url_list})
                self.stdout.write(json.dumps(result))
                return

        self.stdout.write(json.dumps({"result": "all pages already cached", "cached pages": buf_url_list}))