# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from django.core.cache import cache
from django.utils.text import Truncator
from django.utils.html import strip_tags

from haystack.query import SearchQuerySet


TAGS_CACHE_TIME = 3600

def search_tag(search_text):
    if search_text:
        sqs = SearchQuerySet().auto_query(search_text, "text")
        return sqs.best_match() if sqs else None
    return None


def turncat(title, w_count=5, c_count=50, end_ch='...'):

    return Truncator(
        Truncator(strip_tags(title)).words(w_count, truncate=end_ch)
    ).chars(c_count, truncate=end_ch)


def update_hot_tags_on_render(text_block):

    tags = cache.get("hot_tag_list_%s" % text_block.pk)
    if not tags:
        from edw_fluent.plugins.hottag.models import HotTag
        tags = HotTag.objects.filter(object_id=text_block.pk)
        if tags:
            cache.set("hot_tag_list_%s" % text_block.pk, tags, TAGS_CACHE_TIME)
        else:
            # empty
            cache.set("hot_tag_list_%s" % text_block.pk, True, TAGS_CACHE_TIME)

    if not isinstance(tags, bool) and hasattr(text_block, 'text'):
        try:
            soup = BeautifulSoup(text_block.text, 'html.parser')
        except:
            return text_block

        for tag in tags:
            # update tag
            hot_tag = soup.find(attrs={"data-edw-id": "%s" % tag.pk})
            if hot_tag:
                if tag.target_publication:
                    hot_tag['data-edw-model-id'] = tag.target_publication.pk
                    hot_tag['title'] = turncat(tag.target_publication.entity_name)
                    try:
                        hot_tag['href'] = tag.target_publication.get_detail_url()
                    except:
                        hot_tag['href'] = ''

                    if hot_tag['href'] != '':
                        hot_tag.name = 'a'
                    else:
                        hot_tag.name = 'span'
                else:
                    if hot_tag.has_key('data-edw-model-id'):
                        del hot_tag['data-edw-model-id']
                    if hot_tag.has_key('title'):
                        del hot_tag['title']
                    if hot_tag.has_key('href'):
                        del hot_tag['href']
                    if hot_tag.name != 'span':
                        hot_tag.name = 'span'

        if tags:
            try:
                text_block.text = unicode(soup)
            except:
                pass

    return text_block