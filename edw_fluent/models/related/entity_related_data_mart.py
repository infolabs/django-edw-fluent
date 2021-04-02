# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from edw.models.related import BaseEntityRelatedDataMart


class EntityRelatedDataMart(BaseEntityRelatedDataMart):
    key = models.IntegerField(verbose_name=_('Key'), blank=True, null=True, db_index=True)

    """Materialize"""
    class Meta(BaseEntityRelatedDataMart.Meta):
        """
        RUS: Метаданные класса.
        """
        abstract = False
