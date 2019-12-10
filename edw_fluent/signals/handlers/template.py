# -*- coding: utf-8 -*-

import itertools

from django.db.models.signals import (
    pre_delete,
    post_save
)

from edw.signals import make_dispatch_uid
from edw_fluent.models.template.base import BaseTemplate
from edw_fluent.templatetags.edw_fluent_tags import BaseRenderTemplateTag


#==============================================================================
# BaseTemplate and subclass models event handlers
#==============================================================================
def invalidate_entity_after_save(sender, instance, **kwargs):
    """
    Clear templates buffer
    RUS: Очищает буфер template_buffer после сохранения шаблонных тегов.
    """
    BaseRenderTemplateTag.clear_template_buffer()


def invalidate_entity_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает буфер template_buffer после сохранения шаблонных тегов.
    """
    invalidate_entity_after_save(sender, instance, **kwargs)

# отправляет сигналы обработчику после сохранения и перед удалением шаблонных тегов.
Model = BaseTemplate
for clazz in itertools.chain([Model], Model.get_all_subclasses()):
    pre_delete.connect(invalidate_entity_before_delete, clazz,
                       dispatch_uid=make_dispatch_uid(pre_delete, invalidate_entity_before_delete, clazz))
    post_save.connect(invalidate_entity_after_save, clazz,
                      dispatch_uid=make_dispatch_uid(post_save, invalidate_entity_after_save, clazz))
