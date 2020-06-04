# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from page_builder.widgets import PageBuilderWidget

from edw.admin.entity.forms import EntityAdminForm as OriginalEntityAdminForm

from edw_fluent.models.page_layout import get_views_layouts


class BaseTemplateForm(OriginalEntityAdminForm):
    """
    Класс формы базового шаблона
    """
    class Meta:
        """
        RUS: Метаданные класса.
        """
        fields = '__all__'
        widgets = {
            'template': PageBuilderWidget,
        }


class TemplateForm(BaseTemplateForm):
    """
    RUS: Класс формы шаблона.
    """
    messages = {
        'has_view_layout_error': _("The view layout of the publication isn't defined"),
    }

    def clean_terms(self):
        """
        RUS: Словарь проверенных и нормализованных данных формы шаблона.
        Вызывает ошибку валидации формы, если нет
        списка терминов представлений разметок страниц и терминов в очищенных данных.
        """
        terms = self.cleaned_data.get("terms")
        if not (set([v.id for (k, v) in get_views_layouts().items()]) & set([x.id for x in terms])):
            raise forms.ValidationError(self.messages['has_view_layout_error'])
        return terms
