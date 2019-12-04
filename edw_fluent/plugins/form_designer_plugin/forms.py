# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentItemForm

from salmonella.widgets import SalmonellaIdWidget

from form_designer.models import FormDefinition

from edw_fluent.plugins.form_designer_plugin.models import FormDesignerItem


class FormDefinitionForm(ContentItemForm):
    """
    RUS: Класс Форма по созданию формы FormDefinitionForm
    """
    form_definition = forms.ModelChoiceField(
        label=_('Form'),
        queryset=FormDefinition.objects.all(),
        widget = SalmonellaIdWidget(
            FormDesignerItem._meta.get_field("form_definition").rel,
            admin.site,
        ),
        required=True
    )