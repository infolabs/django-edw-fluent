# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentItemForm

from salmonella.widgets import SalmonellaIdWidget

from form_designer.models import FormDefinition

from edw_fluent.plugins.form_designer_plugin.models import FormDesignerItem


try:
    form_definition_rel = FormDesignerItem._meta.get_field("form_definition").rel
except AttributeError:
    form_definition_rel = FormDesignerItem._meta.get_field("form_definition").remote_field


class FormDefinitionForm(ContentItemForm):
    """
    RUS: Класс Форма по созданию формы FormDefinitionForm
    """
    form_definition = forms.ModelChoiceField(
        label=_('Form'),
        queryset=FormDefinition.objects.all(),
        widget = SalmonellaIdWidget(form_definition_rel, admin.site),
        required=True
    )
