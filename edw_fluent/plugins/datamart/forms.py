# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentItemForm
from salmonella.widgets import SalmonellaMultiIdWidget

from edw.admin.term.widgets import TermTreeWidget
from edw.models.term import BaseTerm, TermModel
from edw.models.entity import EntityModel
from edw.models.data_mart import DataMartModel

from edw_fluent.plugins.datamart.models import DataMartItem


class DataMartPluginForm(ContentItemForm):
    """
    RUS: Класс плагина формы витрины данных.
    """
    datamarts = forms.ModelMultipleChoiceField(
        label=_('Data marts'),
        queryset=DataMartModel.objects.all(),
        widget = SalmonellaMultiIdWidget(
            DataMartItem._meta.get_field("datamarts").rel,
            admin.site,
        )
    )

    subjects = forms.ModelMultipleChoiceField(
        label = _('Subjects'),
        queryset=EntityModel.objects.active(),
        widget = SalmonellaMultiIdWidget(
            DataMartItem._meta.get_field("subjects").rel,
            admin.site,
        ),
        required=False
    )

    terms = forms.ModelMultipleChoiceField(
        label = _('Terms'),
        queryset=TermModel.objects.all().exclude(
        system_flags=BaseTerm.system_flags.external_tagging_restriction),
        widget = TermTreeWidget(external_tagging_restriction=False, fix_it=False),
        required=False
    )

    class Media:
        """
        RUS: Статические css-файлы.
        """
        css = {
            'all': [
                '/static/css/admin/entity.css',
            ]
        }
