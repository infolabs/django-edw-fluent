# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fluent_pages.models import PageLayout
from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin
from fluent_pages.integration.fluent_contents.models import FluentContentsPage
from fluent_pages.extensions import PageTypePlugin, page_type_pool

from edw_fluent.plugins.datamart.models import DataMartItem


#===================================================================================================================
# Создаем новый тип страницы SimplePage для FluentPages
#===================================================================================================================
class SimplePage(FluentContentsPage):

    layout = models.ForeignKey(
        PageLayout,
        verbose_name=_('Layout'),
        null=True,
    )
    seo_title = models.CharField(
        verbose_name=_('SEO title'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("Simple page")
        verbose_name_plural = _("Simple pages")
        permissions = (
            ('change_page_layout', _("Can change Page layout")),
        )


#===================================================================================================================
# Добавляем в пул страниц FluentPages модель SimplePage
#===================================================================================================================
@page_type_pool.register
class SimplePagePlugin(PageTypePlugin):
    model = SimplePage
    model_admin = FluentPageAdmin
    sort_priority = 10

    def get_render_template(self, request, simplepage, **kwargs):
        # Allow subclasses to easily override it by specifying `render_template` after all.
        # The default, is to use the template_path from the layout object.
        return self.render_template or simplepage.layout.template_path

    def get_context(self, request, page, **kwargs):
        context = super(SimplePagePlugin, self).get_context(request, page, **kwargs)
        placeholder = page.placeholder_set.filter(slot='main')[0]
        if placeholder:
            datamart_items = DataMartItem.objects.filter(placeholder_id=placeholder.id)
            terms = set()
            for datamart_item in datamart_items:
                if not datamart_item.not_use_for_template_calculate:
                    datamarts_terms = datamart_item.datamarts.distinct().values_list('terms__id', flat=True)
                    datamart_item_terms = datamart_item.terms.values_list('id', flat=True)
                    terms.update(datamarts_terms)
                    terms.update(datamart_item_terms)
            context.update(
                {
                    'terms_ids': list(terms)
                }
            )

        return context