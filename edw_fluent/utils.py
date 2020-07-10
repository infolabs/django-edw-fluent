# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from constance import config


# https://unicode-table.com
DEFAULT_SYMBOL_RANGES = [
    [32, 1280],    # Alphabetical characters (base latin, extend latin, cyrillic)
    [8192, 8399],  # General punctuation, superscript and subscript characters, currency Symbols
    [8448, 8591],  # Letter-like characters, numeric forms
]


# Python 3

try:
    long_type = long
except NameError:
    long_type = int


try:
    chr_type = unichr
except NameError:
    chr_type = chr


def remove_unprintable(text):
    """
    RUS: Удаляет непечатаемый текст.
    """
    symbol_ranges = DEFAULT_SYMBOL_RANGES
    config_ranges = getattr(config, 'PRINTABLE_SYMBOL_RANGES', None)
    if config_ranges is not None:
        try:
            config_ranges = json.loads('[' + config_ranges + ']')
        except ValueError as e:
            raise ValueError("PRINTABLE_SYMBOL_RANGES setting is incorrect: %s" % e)
        else:
            symbol_ranges = config_ranges

    ranges = []
    for r in symbol_ranges:
        ranges += range(*r)

    allowed_chars = ''.join(map(chr_type, ranges))
    return ''.join(filter(lambda x: x in allowed_chars, text))


def get_data_mart_page(datamart_id):
    """
    :param datamart_id: id или slug витрины данных
    :return: возвращает страницу с размещенной на ней заданной витриной данных, если таких
    несколько - вернется первая попавшаяся
    """
    if datamart_id is not None:
        from edw.models.data_mart import DataMartModel
        id_attr = "id" if isinstance(datamart_id, (int, long_type)) else "slug"
        try:
            data_mart = DataMartModel.objects.get(**{id_attr: datamart_id})
        except DataMartModel.DoesNotExist:
            pass
        else:
            return data_mart.get_cached_detail_page()
    return None
