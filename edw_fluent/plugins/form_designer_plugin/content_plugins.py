# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from constance import config

from sekizai.helpers import get_varname as sekizai_get_varname

from fluent_contents.extensions import ContentPlugin, plugin_pool

from form_designer import settings
from form_designer.views import process_form

from edw_fluent.plugins.form_designer_plugin.models import FormDesignerItem
from edw_fluent.plugins.form_designer_plugin.forms import FormDefinitionForm


@plugin_pool.register
class FormDesignerPlugin(ContentPlugin):
    """
    Plugin for rendering Form designer form
    RUS: Класс плагин Дизайнера форм FormDesignerPlugin
    """
    model = FormDesignerItem

    form = FormDefinitionForm

    cache_output = False

    def get_render_template(self, request, instance, **kwargs):
        """
        RUS: Возвращает выбранный из списка шаблон формы для рендеринга,
        если он не выбран - используется шаблон формы по умолчанию.
        """
        if instance.form_definition.form_template_name:
            self.render_template = instance.form_definition.form_template_name
        else:
            self.render_template = settings.DEFAULT_FORM_TEMPLATE

        return self.render_template

    def get_context(self, request, instance, **kwargs):
        """
        Return the context to use in the template defined by ``render_template`` (or :func:`get_render_template`).
        By default, it returns the model instance as ``instance`` field in the template.
        RUS: Возвращает контекст для шаблонов плагина "дизайнер форм".
        """

        sekizai_varname = sekizai_get_varname()

        context = {
            'instance': instance,
            'config': config,
            sekizai_varname: getattr(request, sekizai_varname),
        }

        return process_form(request, instance.form_definition, context, disable_redirection=True)


"""
    def render(self, request, instance, **kwargs):

        render_template = self.get_render_template(request, instance, **kwargs)
        if not render_template:
            return unicode(_(u"{No rendering defined for class '%s'}" % self.__class__.__name__))

        context = self.get_context(request, instance, **kwargs)

        # Redirection does not work with plugin, hence disable:
        return
"""