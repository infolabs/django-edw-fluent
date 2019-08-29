# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def remove_unprintable(text):
    allowed_chars = ''.join(map(unichr, range(32, 1105)))
    return filter(lambda x: x in allowed_chars, text)
