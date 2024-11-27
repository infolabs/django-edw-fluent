# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import re
import json
from constance import config

from django.core.management import call_command


# https://unicode-table.com
DEFAULT_SYMBOL_RANGES = [
    # u0020, u0500
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

def get_allowed_chars():
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

    return ''.join(map(chr_type, ranges))


def remove_unprintable(text):
    """
    RUS: Удаляет непечатаемый текст.
    """
    allowed_chars = get_allowed_chars()
    return ''.join(filter(lambda x: x in allowed_chars, text))


def clean_unprintable(text, filler=r' '):
    """
    RUS: Заменяет непечатаемый текст на заполнитель.
    """
    allowed_chars = get_allowed_chars()
    return ''.join([c if c in allowed_chars else filler for c in text])


emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F1E0-\U0001F1FF"
    u"\U00002500-\U00002BEF"
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"
    u"\u3030"
    "]+",
    flags=re.UNICODE)


def remove_emoji(text, filler=r''):
    return emoji_pattern.sub(filler, text)


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


def get_warming_up_result(urn):
    start_time = time.time()
    result = {
        'urn': urn,
        'elapsed_time': 0,
        'errors': None,
    }
    try:
        call_command('warming_up', urn=urn)
        result['elapsed_time'] = f'{(time.time() - start_time):.2f} sec'
    except Exception as err:
        result['errors'] = str(err)

    return result
