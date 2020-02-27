# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from .utils import search_tag
from edw_fluent.plugins.hottag.models import HotTag
from edw_fluent.plugins.hottag.utils import turncat

try:
    uni_type = unicode
except NameError:
    uni_type = str


def hottag_filter(textitem, html):
    """
    Apply filter to the text.
    RUS: Запускаем парсер BeautifulSoup в формате html.
    Выбираем из результатов парсинга hot_tags со значением еdw-hottag.
    Если есть текстовый блок с первичным ключом, в цикле выбираем теги,
    у которых первичный ключ равен значению атрибута тега data-edw-id.
    Ищем соответствие этому тегу в публикациях, в результате выбирается - 1 публикация наиболее релевантная,
    если соответствие не найдено, то данные этой публикации не сохраняются.
    Проверяется, есть ли уже гиперссылка и заголовок данного тега в публикации, если нет создает тег span и
    сохраняет данный hot_tag в базе данных на определенный срок.
    Если этот hot_tag в найденной публикацией является ссылкой с тегом а, то он удаляется
    """
    soup = BeautifulSoup(html, 'html.parser')
    hot_tags = soup.select('.edw-hottag')
    founded_hot_tags_ids = []

    if textitem.pk:

        for tag in hot_tags:
            e_tag_pk = tag.attrs.get('data-edw-id', None)
            try:
                tag_obj = HotTag.objects.get(pk=e_tag_pk) if e_tag_pk else HotTag()
            except HotTag.DoesNotExist:
                tag_obj = HotTag()

            tag_obj.content_object = textitem
            tag_obj.title = tag.attrs.get('data-edw-tag', '')

            # check if already founded
            target_model_id = tag.attrs.get('data-edw-model-id', None)
            if target_model_id:
                try:
                    PublicationModel = HotTag._meta.get_field('target_publication').rel.to
                    target_publication = PublicationModel.objects.get(pk=target_model_id)
                except:
                    target_publication = None
            else:
                target_publication = None

            if target_publication:
                tag_obj.target_publication = target_publication
            else:
                pid = textitem.parent_id if textitem.parent_id else None
                result = search_tag(tag_obj.title, pid)

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
                    if 'href' in list(tag.keys()):
                        del tag['href']

                if tag.has_key('href'):
                    tag.name = 'a'
                else:
                    tag.name = 'span'
            else:
                if 'data-edw-model-id' in list(tag.keys()):
                    del tag['data-edw-model-id']
                if 'title' in list(tag.keys()):
                    del tag['title']
                if 'href' in list(tag.keys()):
                    del tag['href']
                tag.name = 'span'

            # del tags from db if they were deleted in text
            HotTag.objects.filter(object_id=textitem.pk).exclude(pk__in=founded_hot_tags_ids).delete()

        res = uni_type(soup) if soup and hot_tags else html
    else:
        # make filter after conten item created
        res = html

    return res
