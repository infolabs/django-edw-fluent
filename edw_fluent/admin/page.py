# -*- coding: utf-8 -*-

from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin
from fluent_pages.extensions import PageTypePlugin, page_type_pool

from django.conf import settings
from django.contrib import admin
from django.utils import six
from django.utils.decorators import method_decorator

from edw_fluent.models.page import SimplePage, cache_simple_page
from edw_fluent.admin.forms.page import SimplePageAdminForm
from edw_fluent.plugins.datamart.models import DataMartItem


#===================================================================================================================
# Регистрируем админку SimplePage
#===================================================================================================================
@admin.register(SimplePage)
class SimplePageAdmin(FluentPageAdmin):

    form = SimplePageAdminForm

    exclude = FluentPageAdmin.exclude + ('terms', )

    @property
    def media(self):
        # use local js
        media = super(SimplePageAdmin, self).media
        if six.PY2:
            return media

        for i, m in enumerate(media._js):
            if m == 'fluent_pages/fluentpage/fluent_layouts.js':
                media._js[i] = 'edw_fluent/page/fluent_layouts.js'
                break
        return media

    change_form_template = [
        "edw_fluent/admin/change_form.html",
    ] if six.PY3 else []


#===================================================================================================================
# Добавляем для админки в пул страниц FluentPages модель SimplePage
#===================================================================================================================
@page_type_pool.register
class SimplePagePlugin(PageTypePlugin):
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
