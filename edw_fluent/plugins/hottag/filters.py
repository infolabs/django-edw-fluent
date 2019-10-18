# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from haystack.query import SearchQuerySet

from edw_fluent.plugins.hottag.models import HotTag
from edw_fluent.plugins.hottag.utils import turncat


def hottag_filter(textitem, html):
    """
    Apply filter to the text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    hot_tags = soup.select('.edw-hottag')
    founded_hot_tags_ids = []

    for tag in hot_tags:
        e_tag_pk = tag.attrs.get('data-edw-id', None)
        try:
            tag_obj = HotTag.objects.get(pk=e_tag_pk) if e_tag_pk else HotTag()
        except HotTag.DoesNotExist:
            tag_obj = HotTag()

        tag_obj.content_object = textitem
        tag_obj.title = tag.attrs['data-edw-tag']

        sqs = SearchQuerySet().auto_query(tag_obj.title, "text")
        result = sqs.best_match() if sqs else None

        if result and result.object:
           tag_obj.target_publication = result.object
        else:
            # clear
            tag_obj.target_publication = None

        tag_obj.save()
        founded_hot_tags_ids.append(tag_obj.pk)

        tag['data-edw-id'] = tag_obj.pk
        tag['data-edw-tag'] = tag_obj.title

        if tag_obj.target_publication:
            tag['data-edw-model-id'] = tag_obj.target_publication.pk
            tag['title'] = turncat(tag_obj.target_publication.entity_name)

            try:
                tag['href'] = tag_obj.target_publication.get_detail_url()
            except:
                if tag.has_key('href'):
                    del tag['href']

            if tag.has_key('href'):
                tag.name = 'a'
            else:
                tag.name = 'span'
        else:
            if tag.has_key('data-edw-model-id'):
                del tag['data-edw-model-id']
            if tag.has_key('title'):
                del tag['title']
            if tag.has_key('href'):
                del tag['href']
            tag.name = 'span'

        # del tags from db if they were deleted in text
        HotTag.objects.filter(object_id=textitem.pk).exclude(pk__in=founded_hot_tags_ids).delete()

    res = soup.prettify() if soup else html

    return res