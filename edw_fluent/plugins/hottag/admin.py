# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from edw_fluent.plugins.hottag.models import HotTag


class HotTagAdmin(admin.ModelAdmin):

    model = HotTag

    list_display = ('title', 'content_type', 'object_id', 'content_object', 'target_publication', 'created_at')


admin.site.register(HotTag, HotTagAdmin)