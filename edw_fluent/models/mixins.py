# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from edw_fluent.models.page import SimplePage
from edw_fluent.plugins.datamart.models import DataMartItem


class DataMartFluentMixin(object):

    def get_detail_page(self):
        """
        RUS: Для просмотра содержимого конкретной страницы
        """
        placeholders = DataMartItem.objects.filter(
            datamarts__in=[self.pk]
        ).values_list(
            'placeholder_id',
            flat=True
        )
        try:
            result = SimplePage.objects.filter(
                placeholder_set__id__in=placeholders
            ).exclude(
                translations__override_url='/'
            )[0]
        except IndexError:
            result = None
        return result
