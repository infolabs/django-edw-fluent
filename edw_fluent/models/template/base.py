# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from edw.models.entity import EntityModel


# =========================================================================================================
# BaseTemplate
# =========================================================================================================
class BaseTemplate(EntityModel.materialized):

    ORDER_BY_NAME_ASC = 'basetemplate__name'

    ORDERING_MODES = (
        (ORDER_BY_NAME_ASC, _('Alphabetical')),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        default=''
    )
    index = models.CharField(
        max_length=255,
        verbose_name=_("On indexation"),
        blank=False,
        null=False,
        default=''
    )

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    class RESTMeta:
        exclude = ['images']

    @property
    def entity_name(self):
        return self.name

    def get_template(self):
        return getattr(self, 'template', None)

    def pre_save_entity(self, origin, *args, **kwargs):
        super(BaseTemplate, self).pre_save_entity(origin, *args, **kwargs)

        templates = self.get_template().get_templates()
        self.index = " ".join(templates)
