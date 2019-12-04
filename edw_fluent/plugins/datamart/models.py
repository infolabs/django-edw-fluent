# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fluent_contents.models import ContentItem

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from page_builder.fields import BuilderTemplateField

from edw_fluent.models.page_builder import get_page_builder_elements_by_model


db_table_name_pattern = '{}_{}'.format(settings.EDW_APP_LABEL, '{}')

@python_2_unicode_compatible
class DataMartItem(ContentItem):
    datamarts = models.ManyToManyField(
        'DataMart',
        related_name='datamartitem_datamarts',
        db_table=db_table_name_pattern.format('datamartitem_datamarts')
    )

    subjects = models.ManyToManyField(
        'Entity',
        related_name='datamartitem_subjects',
        db_table=db_table_name_pattern.format('datamartitem_subjects')
    )

    terms = models.ManyToManyField(
        'Term',
        related_name='datamartitem_terms',
        db_table=db_table_name_pattern.format('datamartitem_terms')
    )

    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        blank=True,
        elements=get_page_builder_elements_by_model('DataMartItem'),
    )

    not_use_for_template_calculate = models.BooleanField(
        verbose_name=_('In template calculate flag'),
        help_text=_('Do not use when calculating a template'),
        default=False
    )

    is_cache_output = models.BooleanField(
        verbose_name=_('Сache datamart plugin'),
        help_text=_('Cache datamart plugin on render output'),
        default=True
    )

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Data mart item')
        verbose_name_plural = _('Data mart items')

    def __str__(self):
        result = ('{} #{}').format(self.__class__, self.id)
        # for datamart in self.datamarts.all():
        #     result = result + datamart.name + ' '
        return result
