# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from salmonella.admin import SalmonellaMixin

from edw_fluent.plugins.hottag.models import HotTag


class HotTagAdmin(SalmonellaMixin, admin.ModelAdmin):

    model = HotTag

    list_display = ('title', 'content_type', 'object_id', 'content_block', 'target_publication', 'created_at')

    fields = ['title', 'content_type', 'object_id', 'target_publication']

    salmonella_fields = ('target_publication',)

    def content_block(self, obj):
        return obj.content_object
    content_block.short_description = _('Content block')


admin.site.register(HotTag, HotTagAdmin)