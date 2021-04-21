# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from filer.models import File as FilerFile
from django.db.models import F


class Command(BaseCommand):
    def handle(self, **options):
        print('Renaming files')
        renamed_files_count = FilerFile.objects.filter(original_filename=None).update(original_filename=F('name'))
        print(f'Operation complete. {renamed_files_count} files have been renamed')
