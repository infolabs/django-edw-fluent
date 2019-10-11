# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from constance import config

from sekizai.helpers import get_varname as sekizai_get_varname

from fluent_contents.extensions import ContentPlugin, plugin_pool

from edw.rest.serializers.entity import EntityDetailSerializer
from edw.views.entity import EntityViewSet

from edw_fluent.models.related import EntityImage, EntityFile
from edw_fluent.plugins.block.models import BlockItem
from edw_fluent.plugins.block.forms import BlockPluginForm


@plugin_pool.register
class BlockPlugin(ContentPlugin):
    model = BlockItem

    form = BlockPluginForm

    admin_init_template = "admin/plugins/block/init.html"

    admin_form_template = ContentPlugin.ADMIN_TEMPLATE_WITHOUT_LABELS

    render_template = "edw_fluent/plugins/block.html"

    cache_output = False

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Block')
        verbose_name_plural = _('Block')

    def get_context(self, request, instance, **kwargs):
        context = super(BlockPlugin, self).get_context(request, instance, **kwargs)
        current_index = getattr(request, '_blockitem_index', 0)
        publication = request.GET.get(EntityViewSet.REQUEST_CACHED_SERIALIZED_DATA_KEY, None)
        if publication is None:
            publication_serializer = EntityDetailSerializer(instance.parent, context={"request": request})
            publication = publication_serializer.data
            request.GET[EntityViewSet.REQUEST_CACHED_SERIALIZED_DATA_KEY] = publication

        sekizai_varname = sekizai_get_varname()
        context.update({
            'publication': publication,
            'position': current_index,
            'text': instance.text,
            'subjects': instance.subjects.all(),
            'images': EntityImage.objects.filter(key=str(instance.id)),
            'files': EntityFile.objects.filter(key=str(instance.id)),
            'config': config,
            sekizai_varname: getattr(request, sekizai_varname),
        })
        request._blockitem_index = current_index + 1
        return context
