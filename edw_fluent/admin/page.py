# -*- coding: utf-8 -*-
import six

from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin
from fluent_pages.integration.fluent_contents.page_type_plugins import FluentContentsPagePlugin
from fluent_pages.extensions import page_type_pool

from django.conf import settings
from django.contrib import admin
from django.utils.decorators import method_decorator

from edw_fluent.models.page import SimplePage, cache_simple_page
from edw_fluent.admin.forms.page import SimplePageAdminForm
from edw_fluent.plugins.datamart.models import DataMartItem


#===================================================================================================================
# Регистрируем админку SimplePage
#===================================================================================================================
@admin.register(SimplePage)
class SimplePageAdmin(FluentPageAdmin):

    base_form = SimplePageAdminForm

    @property
    def media(self):
        media = super(SimplePageAdmin, self).media

        # use local js
        for i, m in enumerate(media._js_lists):
            if len(m) == 1 and m[0] == 'fluent_pages/fluentpage/fluent_layouts.js':
                media._js_lists[i] = ('edw_fluent/page/fluent_layouts.js',)
                break
        return media

    change_form_template = [
        "edw_fluent/admin/change_form.html",
    ]


#===================================================================================================================
# Добавляем для админки в пул страниц FluentPages модель SimplePage
#===================================================================================================================
@page_type_pool.register
class SimplePagePlugin(FluentContentsPagePlugin):
    """
    RUS: Плагин для страницы.
    """
    model = SimplePage

    model_admin = SimplePageAdmin

    sort_priority = 10

    def get_render_template(self, request, simplepage, **kwargs):
        """
        RUS: Возвращает шаблон для рендеринга для конкретной страницы или запроса,
        по умолчанию используется путь template_path из макета объекта.
        """
        # Allow subclasses to easily override it by specifying `render_template` after all.
        # The default, is to use the template_path from the layout object.
        return self.render_template or simplepage.layout.template_path

    @method_decorator(cache_simple_page(getattr(settings, 'SIMPLE_PAGE_CACHE_TIMEOUT', 60*10)))
    def get_response(self, request, page, **kwargs):
        """
        RUS: Генерирует вывод страницы.
        """
        return super(SimplePagePlugin, self).get_response(request, page, **kwargs)

    def get_context(self, request, page, **kwargs):
        """
        RUS: Возвращает контекст для использования в шаблоне.
        """
        context = super(SimplePagePlugin, self).get_context(request, page, **kwargs)
        terms_ids_set = set()
        page_terms = page.terms.values_list('id', flat=True)
        if page_terms:
            terms_ids_set.update(page_terms)
        placeholder = page.placeholder_set.filter(slot='main')[0]
        if placeholder:
            datamart_items = DataMartItem.objects.filter(placeholder_id=placeholder.id)
            for datamart_item in datamart_items:
                if not datamart_item.not_use_for_template_calculate:
                    # .exclude(terms__id__isnull=True) нужно для того чтоб на выходе получался список из id терминов
                    # витрины данных, если этого не сделать, а в витрине данных нет терминов, то на выходе получится
                    # список вида [None], что недопустимо при формировании терминов страницы для контекста рендара
                    datamarts_terms = datamart_item.datamarts.distinct() \
                        .exclude(terms__id__isnull=True).values_list('terms__id', flat=True)
                    datamart_item_terms = datamart_item.terms.values_list('id', flat=True)
                    if datamarts_terms:
                        terms_ids_set.update(datamarts_terms)
                    if datamart_item_terms:
                        terms_ids_set.update(datamart_item_terms)
        context.update(
            {
                'terms_ids': list(terms_ids_set) if terms_ids_set else None
            }
        )
        return context
