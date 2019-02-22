# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


DEFAULT_ELEMENTS = {
    'datamartitem': {
        "Data marts": [
            {
                "url": "elements/datamarts/tpl/default_with_tree.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_with_tree.jpg"
            },
            {
                "url": "elements/datamarts/tpl/default_related.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_related.jpg"
            },
            {
                "url": "elements/datamarts/tpl/default_related_with_title.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_related_with_title.jpg"
            }
        ]
    }
}

ELEMENTS = getattr(settings, 'PAGE_BUILDER_PLUGIN_ELEMENTS', DEFAULT_ELEMENTS)

def get_page_builder_elements_by_model(key):
    return ELEMENTS[key] if key in ELEMENTS else {}
