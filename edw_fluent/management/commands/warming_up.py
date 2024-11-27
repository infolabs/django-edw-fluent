import urllib

from edw_fluent.settings import DOMAIN_WITH_PROTOCOL
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _, ugettext


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--urn',
            dest='urn',
            type=str,
            default=None,
            help=ugettext('')
        )

    def handle(self, **options):
        urn = options.get('urn', None)
        if urn is None:
            raise CommandError('Invalid urn value')

        if DOMAIN_WITH_PROTOCOL is None:
            raise CommandError('Site is not configured')

        url = DOMAIN_WITH_PROTOCOL + urn

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.11 (KHTML, like Gecko)'
                          ' Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Connection': 'keep-alive'
        }

        try:
            req = urllib.request.Request(url=url, headers=headers)
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            raise err
