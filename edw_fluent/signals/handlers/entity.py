# -*- coding: utf-8 -*-

import itertools

from django.db.models.signals import (
    pre_delete,
    post_save
)

from edw.models.entity import EntityModel
from edw.signals import make_dispatch_uid
from edw_fluent.models.page import clear_simple_page_buffer, clear_simple_page_url_buffer


#==============================================================================
# EntityModel and subclass models event handlers
#==============================================================================
def invalidate_entity_after_save(sender, instance, **kwargs):
    """
    Clear simple page buffers (primary + url)
    RUS: Очищает буферы simple_page (первичный ``spg_bf`` и URL ``spg_url_bf``)
    после сохранения сущности. Очистка буфера URL синхронно с первичным нужна,
    чтобы плановый прогрев опорных страниц (``warming_up_pages``) не считал уже
    сброшенные страницы закешированными и не «залипал».
    """
    clear_simple_page_buffer()
    clear_simple_page_url_buffer()


def invalidate_entity_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает буфер simple_page_buffer перед удалением сущности.
    """
    invalidate_entity_after_save(sender, instance, **kwargs)

# RUS: Обработчик событий отправляет сигналы после сохранения и перед удалением сущности.
Model = EntityModel.materialized
for clazz in itertools.chain([Model], Model.get_all_subclasses()):
    pre_delete.connect(invalidate_entity_before_delete, clazz,
                       dispatch_uid=make_dispatch_uid(pre_delete, invalidate_entity_before_delete, clazz))
    post_save.connect(invalidate_entity_after_save, clazz,
                      dispatch_uid=make_dispatch_uid(post_save, invalidate_entity_after_save, clazz))
