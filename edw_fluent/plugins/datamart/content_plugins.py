# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import template as django_template

from constance import config

from sekizai.helpers import get_varname as sekizai_get_varname

from fluent_contents.extensions import ContentPlugin, plugin_pool

from edw_fluent.plugins.datamart.models import DataMartItem
from edw_fluent.plugins.datamart.forms import DataMartPluginForm


@plugin_pool.register
class DataMartPlugin(ContentPlugin):
    cache_output = not settings.DEBUG

    model = DataMartItem
    form = DataMartPluginForm
    render_template = "edw_fluent/plugins/datamart.html"

    class Meta:
        verbose_name = _('Data mart')
        verbose_name_plural = _('Data marts')

    def get_context(self, request, instance, **kwargs):
        context = super(DataMartPlugin, self).get_context(request, instance, **kwargs)
        datamarts = instance.datamarts.active()
        terms_ids = list(instance.terms.active().values_list('id', flat=True))
        subj_ids = list(instance.subjects.active().values_list('id', flat=True))
        type_id = instance.polymorphic_ctype_id
        pos = instance.sort_order

        sekizai_varname = sekizai_get_varname()

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
            'request': request,
            'config': config,
            'data_marts': datamarts,
            'data_mart_pk': str(datamarts[0].pk),
            'data_mart_name': datamarts[0].name,
            'terms_ids': terms_ids,
            'subj_ids': subj_ids,
            'is_first': not before,
            'is_last': not after,
            sekizai_varname: getattr(request, sekizai_varname),
        })
        return context

    def render(self, request, instance, **kwargs):
        template_str = instance.template.read_template() if instance.template else None
        if template_str:
            template = django_template.Template(template_str)
            context = django_template.Context(self.get_context(request, instance, **kwargs))
            return template.render(context)
        else:
            return super(DataMartPlugin, self).render(request, instance, **kwargs)

    def get_cached_output(self, placeholder_name, instance):
        # Берем флаг кеширования из инстанции
        return super(DataMartPlugin, self).get_cached_output(placeholder_name, instance) if instance.datamartitem.is_cache_output else None
