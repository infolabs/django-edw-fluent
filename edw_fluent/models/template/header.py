# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from page_builder.fields import BuilderTemplateField

from edw_fluent.models.template.base import BaseTemplate
from edw_fluent.models.page_builder import get_page_builder_elements_by_model


# =========================================================================================================
# HeaderTemplate
# =========================================================================================================
class HeaderTemplate(BaseTemplate):

    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        elements=get_page_builder_elements_by_model('HeaderTemplate'),
        help_text=_("Some help text about header template... `index`, `top`, `bottom`")
    )

    class Meta:
        verbose_name = _("Header Template")
        verbose_name_plural = _("Header Templates")
