# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from edw_fluent.plugins.hottag.views import hottagsearch


urlpatterns = [
    url(r'^hottagsearch/$', hottagsearch, name='hottagsearch'),
]
