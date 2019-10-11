# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import hottagsearch


urlpatterns = [
    url(r'^hottagsearch/$', hottagsearch, name='hottagsearch'),
]
