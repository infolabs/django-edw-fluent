# -*- coding: utf-8 -*-
from django.contrib import admin
from edw_fluent.models.page import SimplePage
from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin


@admin.register(SimplePage)
class SimplePageAdmin(FluentPageAdmin):
    pass
