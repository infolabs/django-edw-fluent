# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentItemForm
from salmonella.widgets import SalmonellaMultiIdWidget

from edw.models.entity import EntityModel

from edw_fluent.models.publication import PublicationBase

from edw_fluent.plugins.block.models import BlockItem


class BlockPluginForm(ContentItemForm):

    subjects = forms.ModelMultipleChoiceField(
        queryset=EntityModel.objects.instance_of(PublicationBase).active(),
        widget=SalmonellaMultiIdWidget(
            BlockItem._meta.get_field("subjects").rel,
            admin.site,
        ),
        required=False,
        help_text=_('Related entity for this block')
    )
