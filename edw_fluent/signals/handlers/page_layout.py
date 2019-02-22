# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models.signals import (
    pre_delete,
    pre_save
)

from fluent_pages.models.db import PageLayout

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
    validate_terms(instance)
    setattr(sender, VIEW_LAYOUT_CACHE_KEY, None)


def invalidate_term_before_delete(sender, instance, **kwargs):
    layout = get_views_layouts().get(instance.key, None)
    if layout is not None:
        layout.hard_delete()
    setattr(sender, VIEW_LAYOUT_CACHE_KEY, None)


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
validate_term_model()
