# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def remove_unprintable(text):
    # Alphabetical chars
    ranges = range(32, 1106)
    # General punctuation
    ranges += range(8192, 8304)
    allowed_chars = ''.join(map(unichr, ranges))
    return filter(lambda x: x in allowed_chars, text)


def get_data_mart_page(datamart_id):
    """
    :param datamart_id: id или slug витрины данных
    :return: возвращает страницу с размещенной на ней заданной витриной данных, если таких
    несколько - вернется первая попавшаяся
    """
    if datamart_id is not None:
        from edw.models.data_mart import DataMartModel
        id_attr = "id" if isinstance(datamart_id, (int, long)) else "slug"
        try:
            data_mart = DataMartModel.objects.get(**{id_attr: datamart_id})
        except DataMartModel.DoesNotExist:
            pass
        else:
            return data_mart.get_cached_detail_page()
    return None
