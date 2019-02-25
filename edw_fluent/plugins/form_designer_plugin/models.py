# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from future.utils import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from form_designer.models import FormDefinition

from fluent_contents.models.db import ContentItem


@python_2_unicode_compatible
class FormDesignerItem(ContentItem):
    form_definition = models.ForeignKey(FormDefinition, verbose_name=_('Form'))

    def __str__(self):
        return self.form_definition.__str__()

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("Form plugin")
        verbose_name_plural = _("Form plugins")
