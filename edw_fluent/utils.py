# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def remove_unprintable(text):
    """
    RUS: Удаляет непечатаемый текст.
    """
    # Alphabetical characters (base latin, extend latin, cyrilic)
    ranges = range(32, 1280)
    # General punctuation, Superscript and subscript characters, Currency Symbols
    ranges += range(8192, 8399)
    # Letter-like characters, Numeric forms
    ranges += range(8448, 8591)
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
