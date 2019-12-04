# -*- coding: utf-8 -*-

import itertools

from django.db.models.signals import (
    pre_delete,
    post_save
)

from edw.models.entity import EntityModel
from edw.signals import make_dispatch_uid
from edw_fluent.models.page import clear_simple_page_buffer


#==============================================================================
# EntityModel and subclass models event handlers
#==============================================================================
def invalidate_entity_after_save(sender, instance, **kwargs):
    """
    Clear simple page buffer
    RUS: Очищает буфер simple_page_buffer после сохранения сущности.
    """
    clear_simple_page_buffer()


def invalidate_entity_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает буфер simple_page_buffer перед удалением сущности.
    """
    invalidate_entity_after_save(sender, instance, **kwargs)

# RUS: Обработчик событий отправляет сигналы до и после удаления сущности.
Model = EntityModel.materialized
for clazz in itertools.chain([Model], Model.get_all_subclasses()):
    pre_delete.connect(invalidate_entity_before_delete, clazz,
                       dispatch_uid=make_dispatch_uid(pre_delete, invalidate_entity_before_delete, clazz))
    post_save.connect(invalidate_entity_after_save, clazz,
                      dispatch_uid=make_dispatch_uid(post_save, invalidate_entity_after_save, clazz))
