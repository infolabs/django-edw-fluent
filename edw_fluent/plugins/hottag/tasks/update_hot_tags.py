# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import shared_task

from datetime import timedelta

from bs4 import BeautifulSoup

from django.utils import timezone

from edw_fluent.plugins.hottag.utils import turncat
from edw_fluent.plugins.hottag.models import HotTag
from edw_fluent.plugins.hottag.utils import search_tag


try:
    uni_type = unicode
except NameError:
    uni_type = str


@shared_task(name='update_hot_tags')
def update_hot_tags(delta_days=0, full_update="false"):
    """
    :param delta_days: количество дней старше которых обновлять
     если 0 обновляюся все
    :param full_update: Если "true" то делает полное обновление
            по умолчанию обновляет только те у которых нет публикаций
    :return:
    RUS: В течение определенного времени (если не было обновления тегов), ищет публикацию, связанную с созданным тегом,
    если находит, - сохраняет тег (вставляет хот-тег).
    Если нет хот-тегов в целевой публикации или было полное обновление,
    ищет хот-тег по заголовку созданного тега в публикациях в текстовом блоке (тип содержимого : текст),
    если находит, то сохраняет его и привязывает хот-тег к данной публикации,
    добавляет тег span и ссылку на оригинальную публикацию.
    Если в найденной публикации у данного тега уже есть гиперссылка с тегом а, то хот-тег не сохраняется.
    Если в результате обновления текста не найден хот-тег, то тег не сохраняется.
    """

    founded_target_count = 0
    empty_target_count = 0
    deleted_tag_count = 0
    updeted_tag_count = 0
    update_errors_count = 0


    full_update = False if full_update == "false" else True


    if delta_days > 0:
        date = timezone.now() - timedelta(days=delta_days)
        tags_qs = HotTag.objects.filter(created_at__lte=date)
        if not full_update:
            tags_qs = tags_qs.filter(target_publication__isnull=True)
    else:
        if not full_update:
            tags_qs = HotTag.objects.filter(target_publication__isnull=True)
        else:
            tags_qs = HotTag.objects.all()

    total_tag_count = tags_qs.count()

    for tag_obj in tags_qs:
        error = False
        # find empty target
        if not tag_obj.target_publication or full_update:
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

        if text_plugin and hasattr(text_plugin, 'text'):
            try:
                soup = BeautifulSoup(text_plugin.text, 'html.parser')
            except:
                update_errors_count = update_errors_count + 1
                continue

            hot_tag = soup.find(attrs={"data-edw-id": "%s" % tag_obj.pk})
            if hot_tag:
                hot_tag['data-edw-id'] = tag_obj.pk
                hot_tag['data-edw-tag'] = tag_obj.title
                if tag_obj.target_publication:
                    hot_tag['data-edw-model-id'] = tag_obj.target_publication.pk
                    hot_tag['title'] = turncat(tag_obj.target_publication.entity_name)
                    try:
                        hot_tag['href'] = tag_obj.target_publication.get_detail_url()
                    except:
                        if hot_tag.has_key('href'):
                            del hot_tag['href']
                else:
                    if hot_tag.has_key('data-edw-model-id'):
                        del hot_tag['data-edw-model-id']
                    if hot_tag.has_key('title'):
                        del hot_tag['title']
                    if hot_tag.has_key('href'):
                        del hot_tag['href']

                if hot_tag.has_key('href'):
                    hot_tag.name = 'a'
                else:
                    hot_tag.name = 'span'

                try:
                    text_plugin.text = uni_type(soup)
                    text_plugin.save()
                except:
                    update_errors_count = update_errors_count + 1
                    continue

                updeted_tag_count = updeted_tag_count + 1

            else:
                # no parent plugin
                try:
                    tag_obj.delete()
                    deleted_tag_count = deleted_tag_count + 1
                except:
                    update_errors_count = update_errors_count + 1
        else:
            # no parent plugin
            try:
                tag_obj.delete()
                deleted_tag_count = deleted_tag_count + 1
            except:
                update_errors_count = update_errors_count + 1


    return {
        'total_tag_count': total_tag_count,
        'founded_target_count': founded_target_count,
        'empty_target_count': empty_target_count,
        'deleted_tag_count': deleted_tag_count,
        'updeted_tag_count': updeted_tag_count,
        'update_errors_count': update_errors_count
    }
