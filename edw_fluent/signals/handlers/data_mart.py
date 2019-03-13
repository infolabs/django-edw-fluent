# -*- coding: utf-8 -*-

import itertools

from django.db.models.signals import (
    pre_delete,
    post_save
)

from edw.signals import make_dispatch_uid
from edw.models.data_mart import DataMartModel

from edw_fluent.models.page import clear_simple_page_buffer

#==============================================================================
# DataMartModel and subclass models event handlers
#==============================================================================
def invalidate_data_mart_after_save(sender, instance, **kwargs):
    # Clear simple page buffer
    clear_simple_page_buffer()


def invalidate_data_mart_before_delete(sender, instance, **kwargs):
    invalidate_data_mart_after_save(sender, instance, **kwargs)


Model = DataMartModel.materialized
for clazz in itertools.chain([Model], Model.get_all_subclasses()):
    pre_delete.connect(invalidate_data_mart_before_delete, clazz,
                       dispatch_uid=make_dispatch_uid(pre_delete, invalidate_data_mart_before_delete, clazz))
    post_save.connect(invalidate_data_mart_after_save, clazz,
                      dispatch_uid=make_dispatch_uid(post_save, invalidate_data_mart_after_save, clazz))

    clazz.validate_term_model()
