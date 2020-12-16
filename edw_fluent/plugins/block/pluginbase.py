# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from constance import config

from sekizai.helpers import get_varname as sekizai_get_varname

from fluent_contents.extensions import ContentPlugin

from edw.rest.serializers.entity import EntityDetailSerializer
from edw.views.entity import EntityViewSet

from edw_fluent.models.related import EntityImage, EntityFile, PublicationComment
from edw_fluent.plugins.block.models import BlockItem
from edw_fluent.plugins.block.forms import BlockPluginForm

try:
    from edw_fluent.plugins.hottag.utils import update_hot_tags_on_render
except:
    pass

# ------------------------------------------------------------------------------------------------------
# BaseBlockPlugin сделано так для того, чтоб можно было наследоваться от этого блока и перекрывать его
# ------------------------------------------------------------------------------------------------------
class BaseBlockPlugin(ContentPlugin):
    """
    RUS: Класс плагина BaseBlockPlugin.
    """
    model = BlockItem

    form = BlockPluginForm

    # В этом шаблоне сделан импорт из шаблонов edw_fluent, чтоб можно было наследовать данный плагин и перекрывать
    # его в конкретном проекте. Иначе доступа к шаблонам не будет, так как не будет импорта плагина и придется
    # копировать их полностью в проекте, для инициализации.
    admin_init_template = "admin/plugins/block/init.html"

    admin_form_template = ContentPlugin.ADMIN_TEMPLATE_WITHOUT_LABELS

    render_template = "edw_fluent/plugins/block.html"

    cache_output = False

    class Meta:
        """
        RUS: Метаданные класса BaseBlockPlugin.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Block')
        verbose_name_plural = _('Block')

    def get_context(self, request, instance, **kwargs):
        """
        RUS: Возвращает контекст с обновленными данными.
        """
        if update_hot_tags_on_render:
            instance = update_hot_tags_on_render(instance)

        context = super(BaseBlockPlugin, self).get_context(request, instance, **kwargs)
        current_index = getattr(request, '_blockitem_index', 0)
        publication = request.GET.get(EntityViewSet.REQUEST_CACHED_SERIALIZED_DATA_KEY, None)
        if publication is None:
            publication_serializer = EntityDetailSerializer(instance.parent, context={"request": request})
            publication = publication_serializer.data
            request.GET[EntityViewSet.REQUEST_CACHED_SERIALIZED_DATA_KEY] = publication

        sekizai_varname = sekizai_get_varname()
        context.update({
            'key': instance.id,
            'publication': publication,
            'position': current_index,
            'text': instance.text,
            'subjects': instance.subjects.all(),
            'images': EntityImage.objects.filter(key=str(instance.id)),
            'files': EntityFile.objects.filter(key=str(instance.id)),
            'comments': PublicationComment.objects.filter(key=str(instance.id)),
            'config': config,
            sekizai_varname: getattr(request, sekizai_varname),
        })
        request._blockitem_index = current_index + 1

        return context
