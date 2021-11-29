# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import rest_framework_filters as filters

from edw_fluent.models.related import EntityFile


class EntityFileFilter(filters.FilterSet):
    """
    EntityImageFilter
    """
    entity = filters.NumberFilter()
    key = filters.NumberFilter()

    class Meta:
        model = EntityFile
        fields = ['entity', 'key']
