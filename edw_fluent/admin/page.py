# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import six
from edw_fluent.models.page import SimplePage
from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin


@admin.register(SimplePage)
class SimplePageAdmin(FluentPageAdmin):

    @property
    def media(self):
        # use local js
        media = super(SimplePageAdmin, self).media
        if six.PY2:
            return media

        for i, m in enumerate(media._js):
            if m == 'fluent_pages/fluentpage/fluent_layouts.js':
                media._js[i] = 'edw_fluent/page/fluent_layouts.js'
                break
        return media

    change_form_template = [
        "edw_fluent/admin/change_form.html",
    ]
