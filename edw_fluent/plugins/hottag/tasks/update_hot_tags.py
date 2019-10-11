# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import shared_task
from edw_fluent.plugins.hottag.utils import turncat
from edw_fluent.plugins.hottag.models import HotTag
from edw_fluent.plugins.hottag.utils import search_tag
from django.utils import timezone
from datetime import timedelta
from bs4 import BeautifulSoup


@shared_task(name='update_hot_tags')
def update_hot_tags(delta_days=0):
    founded_target_count = 0
    empty_target_count = 0
    deleted_tag_count = 0
    updeted_tag_count = 0

    if delta_days > 0:
        date = timezone.now() - timedelta(days=delta_days)
        tags_qs = HotTag.objects.filter(created_at__lte=date)
    else:
        tags_qs = HotTag.objects.all()

    total_tag_count = tags_qs.count()

    for tag_obj in tags_qs:
        try:
            # find empty target
            if not tag_obj.target_publication:
                #search
                result = search_tag(tag_obj.title)
                if result:
                    tag_obj.target_publication = result.object
                    tag_obj.save()
                    founded_target_count = founded_target_count + 1
                else:
                    empty_target_count = empty_target_count + 1

            # update text content

            text_plugin = tag_obj.content_object

            # TODO: in plugin it may by not text field
            if text_plugin and hasattr(text_plugin, 'text'):
                soup = BeautifulSoup(text_plugin.text, 'html.parser')
                hot_tag = soup.find('a', attrs={"data-edw-id": "%s" % tag_obj.pk})

                if hot_tag:
                    hot_tag['data-edw-id'] = tag_obj.pk
                    hot_tag['data-edw-tag'] = tag_obj.title
                    if tag_obj.target_publication:
                        hot_tag['data-edw-model-id'] = tag_obj.target_publication.pk
                        hot_tag['title'] = turncat(tag_obj.target_publication.entity_name)
                        hot_tag['href'] = tag_obj.target_publication.get_detail_url()
                    else:
                        if hot_tag.has_key('data-edw-model-id'):
                            del hot_tag['data-edw-model-id']
                        if hot_tag.has_key('title'):
                            del hot_tag['title']
                        hot_tag['href'] = "#"

                    text_plugin.text = soup.prettify()
                    text_plugin.save()
                    updeted_tag_count = updeted_tag_count + 1
                else:
                    # no parent plugin
                    tag_obj.delete()
                    deleted_tag_count = deleted_tag_count + 1

            else:
                # no parent plugin
                tag_obj.delete()
                deleted_tag_count = deleted_tag_count + 1
        except:
           pass


    return {
        'total_tag_count': total_tag_count,
        'founded_target_count': founded_target_count,
        'empty_target_count': empty_target_count,
        'deleted_tag_count': deleted_tag_count,
        'updeted_tag_count': updeted_tag_count
    }
