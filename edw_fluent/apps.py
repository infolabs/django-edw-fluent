# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class EdwFluentConfig(AppConfig):
    """
    RUS: Класс для настройки конфигурации django-edw-fluent.
    """
    name = 'edw_fluent'
    verbose_name = _("EDW fluent")

    def ready(self):
        # Импорт для инициализации сигнала. Не удалять!
        from .signals import handlers
        from edw_fluent import tasks
