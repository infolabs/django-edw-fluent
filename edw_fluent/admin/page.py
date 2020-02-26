# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import six
from edw_fluent.models.page import SimplePage
from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin


@admin.register(SimplePage)
class SimplePageAdmin(FluentPageAdmin):
    class Media:
        js = ("edw_fluent/page/fluent_layouts.js",) if six.PY3 else ("fluent_pages/fluentpage/fluent_layouts.js",)

    change_form_template = [
        "edw_fluent/admin/change_form.html",
    ]
