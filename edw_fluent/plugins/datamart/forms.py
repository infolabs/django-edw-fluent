# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentItemForm
try:
    from salmonella.widgets import SalmonellaMultiIdWidget
except ImportError:
    from dynamic_raw_id.widgets import DynamicRawIDMultiIdWidget as SalmonellaMultiIdWidget

from edw.admin.term.widgets import TermTreeWidget
from edw.models.term import TermModel
from edw.models.entity import EntityModel
from edw.models.data_mart import DataMartModel

from edw_fluent.plugins.datamart.models import DataMartItem

try:
    datamarts_rel = DataMartItem._meta.get_field("datamarts").rel
except AttributeError:
    datamarts_rel = DataMartItem._meta.get_field("datamarts").remote_field

try:
    subjects_rel = DataMartItem._meta.get_field("subjects").rel
except AttributeError:
    subjects_rel = DataMartItem._meta.get_field("subjects").remote_field


class DataMartPluginForm(ContentItemForm):
    """
    RUS: Класс плагина формы витрины данных.
    """
    datamarts = forms.ModelMultipleChoiceField(
        label=_('Data marts'),
        queryset=DataMartModel.objects.all(),
        widget = SalmonellaMultiIdWidget(datamarts_rel, admin.site)
    )

    subjects = forms.ModelMultipleChoiceField(
        label = _('Subjects'),
        queryset=EntityModel.objects.active(),
        widget = SalmonellaMultiIdWidget(subjects_rel, admin.site),
        required=False
    )

    terms = forms.ModelMultipleChoiceField(
        label = _('Terms'),
        queryset=TermModel.objects.all(),
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
