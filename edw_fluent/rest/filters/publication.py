# -*- coding: utf-8 -*-

import operator
from functools import reduce

from django import forms
from django.db.models import Q

from django_filters.filters import Filter

from edw.forms.fields import BaseListField


class TagField(BaseListField):

    DEFAULT_MAX_LEN = 25

    def __init__(self, *args, **kwargs):
        fields = forms.CharField(max_length=255)
        super(TagField, self).__init__(fields, *args, **kwargs)

    def clean(self, value):
        return super(TagField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            incl, excl = [], []
            for x in data_list:
                # exclude tags start at "!"
                if x[0] == '!' and len(x) > 1:
                    excl.append(x[1:])
                else:
                    incl.append(x)
            return incl, excl
        return None


class TagFilter(Filter):

    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'icontains')
        super(TagFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        """
        Примеры:
        tags=test1,test2,!test3,!test4 - Публикация должна содержать теги test1 и test2,
        но не должна содержать test3 или test4

        tags!=test1,test2,!test3,!test4 - Публикация должна содержать теги test3 или test4,
        но не должна содержать test1 и test2
        """
        if value:
            lookup = '%s__%s' % (self.field_name, self.lookup_expr)
            incl, excl = value
            incl_method, excl_method = 'filter', 'exclude'
            if self.exclude:
                excl_method, incl_method = incl_method, excl_method
            if incl:
                filters = [Q(**{lookup: x}) for x in incl]
                qs = getattr(qs, incl_method)(reduce(operator.and_, filters))
            if excl:
                filters = [Q(**{lookup: x}) for x in excl]
                qs = getattr(qs, excl_method)(reduce(operator.or_, filters))
            if self.distinct:
                qs = qs.distinct()
        return qs
