# -*- coding: utf-8 -*-

from django.db.models.signals import (
    pre_delete,
)
from edw.signals.mptt import (
    move_to_done,
    post_save
)

from edw.signals import make_dispatch_uid
from edw.models.term import TermModel

from edw_fluent.models.page import clear_simple_page_buffer


#==============================================================================
# TermModel event handlers
#==============================================================================
def invalidate_term_after_save(sender, instance, **kwargs):
    """
    Clear simple page buffer
    RUS: Очищает буфер simple_page_buffer после сохранения терминов.
    """
    clear_simple_page_buffer()


def invalidate_term_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает буфер simple_page_buffer перед удалением терминов.
    """
    invalidate_term_after_save(sender, instance, **kwargs)


def invalidate_term_after_move(sender, instance, target, position, prev_parent, **kwargs):
    """
    RUS: Очищает буфер simple_page_buffer после сохранения перемещенных терминов.
    """
    invalidate_term_after_save(sender, instance, **kwargs)

# RUS: Обработчик событий отправляет сигналы после сохранения, перед удалением и после перемещения терминов.
Model = TermModel.materialized

post_save.connect(invalidate_term_after_save, sender=Model,
                  dispatch_uid=make_dispatch_uid(
                      post_save,
                      invalidate_term_after_save,
                      Model
                  ))
pre_delete.connect(invalidate_term_before_delete, sender=Model,
                   dispatch_uid=make_dispatch_uid(
                       pre_delete,
                       invalidate_term_before_delete,
                       Model
                   ))
move_to_done.connect(invalidate_term_after_move, sender=Model,
                     dispatch_uid=make_dispatch_uid(
                         move_to_done,
                         invalidate_term_after_move,
                         Model
                     ))
