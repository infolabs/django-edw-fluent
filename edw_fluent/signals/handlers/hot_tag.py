# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from edw_fluent.plugins.hottag.filters import hottag_filter
from edw_fluent.plugins.block.models import BlockItem


@receiver(post_save, sender=BlockItem)
def hottag_filter_after_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if hasattr(instance, 'text'):
            try:
                instance.text = hottag_filter(instance, instance.text)
                instance.save()
            except:
                pass