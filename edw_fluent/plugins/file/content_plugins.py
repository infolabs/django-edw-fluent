# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentPlugin, plugin_pool

from edw_fluent.plugins.file.models import FileItem


@plugin_pool.register
class FilePlugin(ContentPlugin):
    model = FileItem
    category = _('Media')
    render_template = 'edw_fluent/plugins/file.html'

    def get_context(self, request, instance, **kwargs):
        context = super(FilePlugin, self).get_context(request, instance, **kwargs)

        type_id = instance.polymorphic_ctype_id
        pos = instance.sort_order

        if pos == 0:
            before = False
        else:
            before = instance.placeholder.contentitems.filter(
                polymorphic_ctype_id=type_id,
                sort_order__exact=pos - 1
            ).exists()

        after = instance.placeholder.contentitems.filter(
            polymorphic_ctype_id=type_id,
            sort_order__exact=pos + 1
        ).exists()

        context.update({
            'file': instance.file,
            'target': instance.target,
            'ext': os.path.splitext(instance.file.name)[1][1:],
            'is_first': not before,
            'is_last': not after
        })

        return context
