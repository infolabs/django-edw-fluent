# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from edw.admin.entity import EntityChildModelAdmin, EntityParentModelAdmin

from edw_fluent.models.template.base import BaseTemplate
from edw_fluent.models.template.header import HeaderTemplate
from edw_fluent.models.template.footer import FooterTemplate

from edw_fluent.admin.forms.template import BaseTemplateForm, TemplateForm


class TemplateAdminMixin(EntityChildModelAdmin):
    """
    Административная панель для создания/изменения шаблонов
    """
    save_on_top = True

    base_fieldsets = (
        (None, {'fields': ('name', 'template', 'index')}),
    )

    search_fields = ['template__name', 'position']
    list_display = ['name', 'created_at', 'index', 'active']
    readonly_fields = ['index']
    exclude = ['entity_name']
    inlines = []

    class Media:
        """
        Подключаемые стили CSS
        """
        css = {'all': ['/static/css/admin/entity.css']}


class HeaderTemplateAdmin(TemplateAdminMixin):
    """
    Административная панель для создания/изменения шаблонов header (шапки), определены базовая модель и базовый шаблон,
    поля наследуется из TemplateAdminMixin
    """
    base_model = HeaderTemplate
    base_form = TemplateForm


class FooterTemplateAdmin(TemplateAdminMixin):
    """
    Административная панель для создания/изменения шаблонов footer (подвала), определены базовая модель и базовый шаблон,
    поля наследуется из TemplateAdminMixin
    """
    base_model = FooterTemplate
    base_form = TemplateForm


class BaseTemplateAdminMixin(EntityParentModelAdmin):
    """
    Административная панель базового шаблона
    """
    base_model = BaseTemplate
    base_form = BaseTemplateForm

    child_models = (
        HeaderTemplate,
        FooterTemplate,
    )

    list_display = ['name', 'get_type', 'active']
    search_fields = ['name']


admin.site.register(HeaderTemplate, HeaderTemplateAdmin) # Регистрация модели
admin.site.register(FooterTemplate, FooterTemplateAdmin) # Регистрация модели

