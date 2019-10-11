# -*- coding: utf-8 -*-
from django.utils.text import Truncator
from django.utils.html import strip_tags
from haystack.query import SearchQuerySet


def search_tag(search_text):
    if search_text:
        sqs = SearchQuerySet().auto_query(search_text, "text")
        return sqs.best_match() if sqs else None
    return None


def turncat(title, w_count=5, c_count=20, end_ch='...'):

    return Truncator(
        Truncator(strip_tags(title)).words(w_count, truncate=end_ch)
    ).chars(c_count, truncate=end_ch)