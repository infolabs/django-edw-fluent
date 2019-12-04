# -*- coding: utf-8 -*-

from django.db.models.signals import (
    pre_delete,
    post_save
)

from edw.signals import make_dispatch_uid

from edw_fluent.models.page import SimplePage, clear_simple_page_buffer


#==============================================================================
# SimplePage event handlers
#==============================================================================
def invalidate_simple_page_after_save(sender, instance, **kwargs):
    """
    Clear simple page buffer
    RUS: Очищает буфер simple_page_buffer после сохранения страницы.
    """
    clear_simple_page_buffer()


def invalidate_simple_page_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает буфер simple_page_buffer перед удалением страницы.
    """
    invalidate_simple_page_after_save(sender, instance, **kwargs)


Model = SimplePage
# отправляет сигналы обработчику SimplePage перед сохраненим и удалением страницы.
post_save.connect(invalidate_simple_page_after_save, sender=Model,
                  dispatch_uid=make_dispatch_uid(
                      post_save,
                      invalidate_simple_page_after_save,
                      Model
                  ))
pre_delete.connect(invalidate_simple_page_before_delete, sender=Model,
                   dispatch_uid=make_dispatch_uid(
                       pre_delete,
                       invalidate_simple_page_before_delete,
                       Model
                   ))
