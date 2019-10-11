# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from haystack.query import SearchQuerySet
from .models import HotTag
from .utils import turncat

def hottag_filter(textitem, html):
    """
    Apply filter to the text.
    """

    soup = BeautifulSoup(html, 'html.parser')
    hot_tags = soup.find_all('a', 'edw-hottag')
    for tag in hot_tags:
        try:
            e_tag_pk = tag.attrs.get('data-edw-id', None)
            try:
                tag_obj = HotTag.objects.get(pk=e_tag_pk) if e_tag_pk else HotTag()
            except:
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

            tag['data-edw-id'] = tag_obj.pk
            tag['data-edw-tag'] = tag_obj.title

            if tag_obj.target_publication:
                tag['data-edw-model-id'] = tag_obj.target_publication.pk
                tag['title'] = turncat(tag_obj.target_publication.entity_name)
                tag['href'] = tag_obj.target_publication.get_detail_url()
            else:
                if tag.has_key('data-edw-model-id'):
                    del tag['data-edw-model-id']
                if tag.has_key('title'):
                    del tag['title']
                tag['href'] = "#"

        except:
            pass

    res = soup.prettify() if soup else html

    return res