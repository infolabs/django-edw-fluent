# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf import settings
from django import template as django_template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from constance import config

from sekizai.helpers import get_varname as sekizai_get_varname

from fluent_contents.extensions import ContentPlugin, plugin_pool

from edw_fluent.models.page import SimplePage
from edw_fluent.plugins.template.models import TemplateItem


@plugin_pool.register
class TemplatePlugin(ContentPlugin):
    """
    RUS: Класс плагина шаблона TemplatePlugin.
    """
    cache_output = not settings.DEBUG

    model = TemplateItem

    class Meta:
        """
        RUS: Метаданные класса TemplatePlugin.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Block')
        verbose_name_plural = _('Block')

    def render(self, request, instance, **kwargs):
        """
        RUS: Возвращает результат обработки html шаблонов,
        если страница была создана и сохранена, был добавлен шаблон и обновлен контекст.
        """
        template_str = instance.template.read_template()

        sekizai_varname = sekizai_get_varname()
        if template_str:
            template = django_template.Template(template_str)
            context = django_template.Context(self.get_context(request, instance, **kwargs))
            context.update(
                {
                    'config': config,
                    'request': request,
                    sekizai_varname: getattr(request, sekizai_varname),
                }
            )

            page_id = instance.placeholder.parent_id
            if page_id:
                try:
                    page = SimplePage.objects.get(id=page_id)
                except SimplePage.DoesNotExist:
                    page = None
                if page:
                    context.update({'page': page})

            return template.render(context)
        else:
            return mark_safe(self.render_error(_('Template is not defined')))
