# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.conf import settings

from edw_fluent.views.publication import PublicationViewSet


# get entity detail view for publications article
publication_detail = PublicationViewSet.as_view(
    {'get': 'retrieve'},
    template_name='/{}/publications/detail.html'.format(settings.EDW_APP_LABEL),
    format='html',
)

urlpatterns = [
    url(r'', include('fluent_pages.urls')),
    url(r'^(?:(?P<path>.+?)/)?(?P<pk>\d+).html$', publication_detail, name='publication_detail'),
]
