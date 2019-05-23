# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import copy

from django import template as django_template
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.conf import settings
from django.apps import AppConfig

from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument, Argument
from classytags.helpers import InclusionTag

from fluent_contents.models.db import Placeholder

from edw.models.entity import EntityModel
from edw.models.term import TermModel
from edw.utils.circular_buffer_in_cache import RingBuffer, empty
from edw.utils.hash_helpers import hash_unsorted_list, create_hash


from edw_fluent.models.template.header import HeaderTemplate
from edw_fluent.models.template.footer import FooterTemplate
from edw_fluent.models.page_layout import get_views_layouts, PAGE_LAYOUT_ROOT_TERM_SLUG

from edw_fluent.models.template.content_block import ContentBlockTemplate
from edw_fluent.models.publication import PublicationBase

register = django_template.Library()


#==============================================================================
# Template selector tags
#==============================================================================
class BaseRenderTemplateTag(Tag):

    TEMPLATE_BUFFER_CACHE_KEY = 'tpl_bf'
    TEMPLATE_BUFFER_CACHE_SIZE = getattr(settings, 'TEMPLATE_BUFFER_CACHE_SIZE', 500)
    TEMPLATE_CACHE_KEY_PATTERN = 'tpl_i:{layout}:{alias_hash}:{terms_hash}'
    TEMPLATE_CACHE_TIMEOUT = getattr(settings, 'TEMPLATE_CACHE_TIMEOUT', 3600)

    template_queryset = EntityModel.objects.active()

    template_model = None

    options = Options(
        MultiKeywordArgument('kwargs', required=False),
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def get_template_queryset(self):
        """
        Get the list of templates for this Tag.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.
        """
        assert self.template_model is not None, (
            "'%s' should either include a `template_model` attribute, "
            "or override the `get_template_queryset()` method."
            % self.__class__.__name__
        )
        queryset = self.template_queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        queryset = queryset.instance_of(self.template_model)

        return queryset

    def get_template(self, alias, layout=None, terms=None):
        """
        Returns the template.
        """
        queryset = self.get_template_queryset().filter(
            **{"{}___index__icontains".format(self.template_model._meta.object_name): alias})

        # clear creation date, time terms & e.t.
        terms = list(TermModel.objects.filter(id__in=terms).exclude(
            system_flags=TermModel.system_flags.external_tagging_restriction).values_list('id', flat=True)
        ) if terms is not None else []

        if layout is not None:
            layout_term = get_views_layouts().get(layout, None)
            if layout_term is not None:
                terms.append(layout_term.id)

        return queryset.semantic_filter(
            terms, use_cached_decompress=True).get_similar(terms, use_cached_decompress=True, fix_it=True)

    @staticmethod
    def get_template_buffer():
        return RingBuffer.factory(BaseRenderTemplateTag.TEMPLATE_BUFFER_CACHE_KEY,
                                  max_size=BaseRenderTemplateTag.TEMPLATE_BUFFER_CACHE_SIZE)

    @staticmethod
    def clear_template_buffer():
        buf = BaseRenderTemplateTag.get_template_buffer()
        keys = buf.get_all()
        buf.clear()
        cache.delete_many(keys)

    def get_cached_template(self, alias, layout=None, terms=None):
        key = BaseRenderTemplateTag.TEMPLATE_CACHE_KEY_PATTERN.format(**{
            "layout": layout if layout else '',
            "alias_hash": create_hash(
                ':'.join([self.template_model._meta.object_name, alias])),
            "terms_hash": hash_unsorted_list(terms) if terms else ''

        })
        template = cache.get(key, empty)
        if template == empty:
            template = self.get_template(alias, layout, terms)
            cache.set(key, template, BaseRenderTemplateTag.TEMPLATE_CACHE_TIMEOUT)
            buf = BaseRenderTemplateTag.get_template_buffer()
            old_key = buf.record(key)
            if old_key != buf.empty:
                cache.delete(old_key)
        return template

    def render_tag(self, context, kwargs, varname):

        alias = kwargs.get('alias', 'index')

        template = self.get_cached_template(
            alias, kwargs.get('layout', PAGE_LAYOUT_ROOT_TERM_SLUG), kwargs.get('terms_ids'))

        if template is not None:
            ctx = copy.copy(context)
            ctx.update({
                "params": kwargs
            })
            template_string = template.template.read_template(alias)
            t = django_template.Template(template_string)
            c = django_template.Context(ctx)
            data = t.render(c)
        else:
            data = ''
        if varname:
            context[varname] = data
            return ''
        else:
            return data


class RenderHeader(BaseRenderTemplateTag):
    name = 'render_header'
    template_model = HeaderTemplate


register.tag(RenderHeader)


class RenderFooter(BaseRenderTemplateTag):
    name = 'render_footer'
    template_model = FooterTemplate


register.tag(RenderFooter)


class RenderContentBlock(BaseRenderTemplateTag):
    name = 'render_content_block'
    template_model = ContentBlockTemplate

    def render_tag(self, context, kwargs, varname):
        kwargs['layout'] = PublicationBase.LAYOUT_TERM_SLUG
        return super(RenderContentBlock, self).render_tag(context, kwargs, varname)


register.tag(RenderContentBlock)


#==============================================================================
# Render Placeholder Field
#==============================================================================
class RenderPlaceholderField(InclusionTag):
    """
    Inclusion tag for static placeholder.
    """

    template = 'edw_fluent/partials/_renderplaceholder.html'
    name = 'render_placeholder_field'

    options = Options(
        Argument('placeholder_id', resolve=True),
    )

    def get_context(self, context, placeholder_id):

        placeholder_object = Placeholder.objects.get(id=placeholder_id)
        context.update({
            'placeholder_object': placeholder_object
        })
        return context


register.tag(RenderPlaceholderField)


#==============================================================================
# Get data mart url
#==============================================================================
class DataMartUrl(Tag):

    name = 'get_data_mart_url'

    options = Options(
        Argument('datamart_id', resolve=True),
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def render_tag(self, context, datamart_id, varname):
        model = AppConfig.get_model('DataMart')
        if not datamart_id:
            datamart_id = None
        try:
            data_mart = model.objects.get(id=datamart_id)
        except model.DoesNotExist:
            detail_page = None
        else:
            detail_page = data_mart.get_cached_detail_page()
        if detail_page:
            detail_url = detail_page.url
        else:
            detail_url = None
        if varname:
            context[varname] = detail_url
            return ''
        else:
            return detail_url


register.tag(DataMartUrl)
