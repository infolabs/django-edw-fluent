# -*- coding: utf-8 -*-
from django.contrib import admin
from edw_fluent.models.page import SimplePage
from fluent_pages.adminui import PageParentAdmin


admin.site.register(SimplePage, admin_class=PageParentAdmin)
