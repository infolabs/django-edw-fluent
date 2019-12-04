# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.db.models.signals import (
    pre_delete,
    pre_save
)
from fluent_pages.models.db import PageLayout

from edw.models.entity import EntityModel
from edw.signals import make_dispatch_uid
from edw_fluent.models.page_layout import (
    VIEW_LAYOUT_CACHE_KEY,
    get_views_layouts,
    validate_term_model,
    validate_terms
)


#==============================================================================
# Event handlers
#==============================================================================
def invalidate_term_before_save(sender, instance, **kwargs):
    """
    RUS: Очищает ключ кеша макета отображения после сохранения терминов.
    """
    validate_terms(instance)
    setattr(sender, VIEW_LAYOUT_CACHE_KEY, None)


def invalidate_term_before_delete(sender, instance, **kwargs):
    """
    RUS: Очищает ключ кеша макета отображения перед удалением терминов.
    """
    layout = get_views_layouts().get(instance.key, None)
    if layout is not None:
        layout.hard_delete()
    setattr(sender, VIEW_LAYOUT_CACHE_KEY, None)

# отправляет сигналы обработчику PageLayout (макету страницы) перед сохраненим и перед удалением терминов.
pre_save.connect(
    invalidate_term_before_save,
    sender=PageLayout,
    dispatch_uid=make_dispatch_uid(
        pre_save,
        invalidate_term_before_save,
        PageLayout
    )
)
pre_delete.connect(
    invalidate_term_before_delete,
    sender=PageLayout,
    dispatch_uid=make_dispatch_uid(
        pre_delete,
        invalidate_term_before_delete,
        PageLayout
    )
)


#==============================================================================
# Call PageLayout model validation (hack for non Entity model)
#==============================================================================
# Устанавливаем таймаут для валидации
key = 'vldt:page_layout:cls'
is_valid = cache.get(key, False)
if not is_valid:
    cache.set(key, True, EntityModel.VALIDATE_TERM_MODEL_CACHE_TIMEOUT)
    validate_term_model()
