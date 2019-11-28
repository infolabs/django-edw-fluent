# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from future.utils import python_2_unicode_compatible

from edw_fluent.plugins.hottag.utils import turncat


@python_2_unicode_compatible
class HotTag(models.Model):
    title = models.CharField(_('Title'), max_length=255, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content type'))
    object_id = models.PositiveIntegerField(verbose_name=_('ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    target_publication = models.ForeignKey('Entity', blank=True, null=True, on_delete=models.SET_NULL,
                                           verbose_name=_('Publication'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Created at'))

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Hot tag')
        verbose_name_plural = _('Hot tags')

    def __str__(self):
        if self.target_publication:
            return _("`{}` → `{}`").format(turncat(self.title), self.target_publication.title)
        return _("`{}` → ").format(turncat(self.title))


