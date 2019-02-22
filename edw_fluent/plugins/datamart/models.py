# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from fluent_contents.models import ContentItem

from page_builder.fields import BuilderTemplateField


ELEMENTS = {
    "Data marts": [
        {
            "url": "elements/datamarts/tpl/default_with_tree.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/default_with_tree.jpg"
        },
        {
            "url": "elements/datamarts/tpl/default_related.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/default_related.jpg"
        },
        {
            "url": "elements/datamarts/tpl/default_related_with_title.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/default_related_with_title.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-1.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-1.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-2.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-2.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-3.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-3.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-4.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-4.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-5.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-5.jpg"
        },
        {
            "url": "elements/datamarts/tpl/main_news-6.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/main_news-6.jpg"
        },
        {
            "url": "elements/datamarts/tpl/popular_tape_recomended.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/popular_tape_recomended.jpg"
        },
        {
            "url": "elements/datamarts/tpl/recommended_popular.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/recommended_popular.jpg"
        },
        {
            "url": "elements/datamarts/tpl/popular_recommended_archive.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/popular_recommended_archive.jpg"
        },
        {
            "url": "elements/datamarts/tpl/digest.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/digest.jpg"
        },
        {
            "url": "elements/datamarts/tpl/digest-2.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/digest-2.jpg"
        },
        {
            "url": "elements/datamarts/tpl/digest-3.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/digest-3.jpg"
        },
        {
            "url": "elements/datamarts/tpl/digest-4.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/digest-4.jpg"
        },
        {
            "url": "elements/datamarts/tpl/digest-5.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/digest-5.jpg"
        },
        {
            "url": "elements/datamarts/tpl/short_news.html",
            "height": 150,
            "thumbnail": "elements/datamarts/thumbs/short_news.jpg"
        },
        {
            "url": "elements/datamarts/tpl/carousel.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/carousel.jpg"
        },
        {
            "url": "elements/datamarts/tpl/list.html",
            "height": 347,
            "thumbnail": "elements/datamarts/thumbs/list.jpg"
        },
        {
            "url": "elements/datamarts/tpl/structure.html",
            "height": 882,
            "thumbnail": "elements/datamarts/thumbs/structure.jpg"
        },
        {
            "url": "elements/datamarts/tpl/partners.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/partners.jpg"
        },
        {
            "url": "elements/datamarts/tpl/advertising_horizontal.html",
            "height": 512,
            "thumbnail": "elements/datamarts/thumbs/advertizing-horizontal.jpg"
        },
        {
            "url": "elements/datamarts/tpl/persons.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/persons.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-main-header.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-main-header.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-materials-slider.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-materials-slider.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-big-slider.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-big-slider.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-datamart.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-datamart.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-daily-slider.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-daily-slider.jpg"
        },
        {
            "url": "elements/datamarts/tpl/dsit-project-management.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/dsit-project-management.jpg"
        },
        {
            "url": "elements/datamarts/tpl/ob-projects-slider.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/ob-projects-slider.jpg"
        },
        {
            "url": "elements/datamarts/tpl/poll.html",
            "height": 312,
            "thumbnail": "elements/datamarts/thumbs/poll.jpg"
        },
    ],
}

@python_2_unicode_compatible
class DataMartItem(ContentItem):
    datamarts = models.ManyToManyField('DataMart', related_name='datamartitem_datamarts', db_table='alder_datamartitem_datamarts')
    subjects = models.ManyToManyField('Entity', related_name='datamartitem_subjects', db_table='alder_datamartitem_subjects')
    terms = models.ManyToManyField('Term', related_name='datamartitem_terms', db_table='alder_datamartitem_terms')
    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        blank=True,
        elements=ELEMENTS,
    )
    not_use_for_template_calculate = models.BooleanField(verbose_name=_('In template calculate flag'), help_text=_('Do not use when calculating a template'), default=False)
    is_cache_output = models.BooleanField(verbose_name=_('Сache datamart plugin'), help_text=_('Cache datamart plugin on render output'), default=True)

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Data mart item')
        verbose_name_plural = _('Data mart items')

    def __str__(self):
        result = ('{} #{}').format(self.__class__, self.id)
        # for datamart in self.datamarts.all():
        #     result = result + datamart.name + ' '
        return result
