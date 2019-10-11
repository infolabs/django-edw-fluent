# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from future.utils import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .utils import turncat


@python_2_unicode_compatible
class HotTag(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    target_publication = models.ForeignKey('Entity', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Hot tag')
        verbose_name_plural = _('Hot tags')

    def __str__(self):
        return turncat(self.title)


