# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

from fluent_contents.models import ContentItem

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from page_builder.fields import BuilderTemplateField

from edw_fluent.models.page_builder import get_page_builder_elements_by_model


@python_2_unicode_compatible
class TemplateItem(ContentItem):
    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        blank=True,
        elements=get_page_builder_elements_by_model('TemplateItem'),
    )
    is_cache_output = models.BooleanField(
        verbose_name=_('Сache template plugin'),
        help_text=_('Cache template plugin on render output'),
        default=True
    )

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return "{}: {}".format(self._meta.verbose_name, self.template)
