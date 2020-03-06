# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdminForm

from django import forms
from django.utils.translation import ugettext_lazy as _

from edw.models.term import TermModel
from edw.admin.term.widgets import TermTreeWidget


class SimplePageAdminForm(FluentPageAdminForm):

    terms = forms.ModelMultipleChoiceField(
        label = _('Terms'),
        queryset=TermModel.objects.all(),
        widget = TermTreeWidget(external_tagging_restriction=False, fix_it=False),
        required=False
    )
