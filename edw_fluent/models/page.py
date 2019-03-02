# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import (
    method_decorator, decorator_from_middleware_with_args,
)
from django.utils.cache import (
    get_max_age, has_vary_header, learn_cache_key as origin_learn_cache_key,
    patch_response_headers,
)

from fluent_pages.models import PageLayout
from fluent_pages.pagetypes.fluentpage.admin import FluentPageAdmin
from fluent_pages.integration.fluent_contents.models import FluentContentsPage
from fluent_pages.extensions import PageTypePlugin, page_type_pool

from edw.utils.circular_buffer_in_cache import RingBuffer

from edw_fluent.plugins.datamart.models import DataMartItem


# =========================================================================================================
# Catch Simple Page cache key
# =========================================================================================================
SIMPLE_PAGE_BUFFER_CACHE_KEY = 'spg_bf'
SIMPLE_PAGE_BUFFER_CACHE_SIZE = getattr(settings, 'SIMPLE_PAGE_BUFFER_CACHE_SIZE', 100)


def get_simple_page_buffer():
    return RingBuffer.factory(SIMPLE_PAGE_BUFFER_CACHE_KEY,
                              max_size=SIMPLE_PAGE_BUFFER_CACHE_SIZE)


def clear_simple_page_buffer():
    buf = get_simple_page_buffer()
    keys = buf.get_all()
    buf.clear()
    cache.delete_many(keys)


# Monkey path: save cache_key for invalidation
def learn_cache_key(request, response, timeout, key_prefix, cache):
    cache_key = origin_learn_cache_key(request, response, timeout, key_prefix, cache)

    # reduce cache
    buf = get_simple_page_buffer()
    old_key = buf.record(cache_key)
    if old_key != buf.empty:
        cache.delete(old_key)

    return cache_key


class SimplePageCacheMiddleware(CacheMiddleware):

    # path `learn_cache_key`, method code equal with origin
    def process_response(self, request, response):
        """Sets the cache, if needed."""
        if not self._should_update_cache(request, response):
            # We don't need to update the cache, just return.
            return response

        if response.streaming or response.status_code != 200:
            return response

        # Don't cache responses that set a user-specific (and maybe security
        # sensitive) cookie in response to a cookie-less request.
        if not request.COOKIES and response.cookies and has_vary_header(response, 'Cookie'):
            return response

        # Try to get the timeout from the "max-age" section of the "Cache-
        # Control" header before reverting to using the default cache_timeout
        # length.
        timeout = get_max_age(response)
        if timeout is None:
            timeout = self.cache_timeout
        elif timeout == 0:
            # max-age was set to 0, don't bother caching.
            return response
        patch_response_headers(response, timeout)
        if timeout:
            cache_key = learn_cache_key(request, response, timeout, self.key_prefix, cache=self.cache)
            if hasattr(response, 'render') and callable(response.render):
                response.add_post_render_callback(
                    lambda r: self.cache.set(cache_key, r, timeout)
                )
            else:
                self.cache.set(cache_key, response, timeout)
        return response


def cache_simple_page(*args, **kwargs):
    """
    Decorator for views that tries getting the page from the cache and
    populates the cache if the page isn't in the cache yet.

    The cache is keyed by the URL and some data from the headers.
    Additionally there is the key prefix that is used to distinguish different
    cache areas in a multi-site setup. You could use the
    get_current_site().domain, for example, as that is unique across a Django
    project.

    Additionally, all headers from the response's Vary header will be taken
    into account on caching -- just like the middleware does.
    """
    # We also add some asserts to give better error messages in case people are
    # using other ways to call cache_page that no longer work.
    if len(args) != 1 or callable(args[0]):
        raise TypeError("cache_page has a single mandatory positional argument: timeout")
    cache_timeout = args[0]
    cache_alias = kwargs.pop('cache', None)
    key_prefix = kwargs.pop('key_prefix', None)
    if kwargs:
        raise TypeError("cache_page has two optional keyword arguments: cache and key_prefix")

    return decorator_from_middleware_with_args(SimplePageCacheMiddleware)(
        cache_timeout=cache_timeout, cache_alias=cache_alias, key_prefix=key_prefix
    )


#===================================================================================================================
# Создаем новый тип страницы SimplePage для FluentPages
#===================================================================================================================
class SimplePage(FluentContentsPage):

    layout = models.ForeignKey(PageLayout, verbose_name=_('Layout'), null=True)

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("Simple page")
        verbose_name_plural = _("Simple pages")
        permissions = (
            ('change_page_layout', _("Can change Page layout")),
        )


#===================================================================================================================
# Добавляем в пул страниц FluentPages модель SimplePage
#===================================================================================================================
@page_type_pool.register
class SimplePagePlugin(PageTypePlugin):
    model = SimplePage
    model_admin = FluentPageAdmin
    sort_priority = 10

    def get_render_template(self, request, simplepage, **kwargs):
        # Allow subclasses to easily override it by specifying `render_template` after all.
        # The default, is to use the template_path from the layout object.
        return self.render_template or simplepage.layout.template_path

    @method_decorator(cache_simple_page(getattr(settings, 'SIMPLE_PAGE_CACHE_TIMEOUT', 60*10)))
    def get_response(self, request, page, **kwargs):
        return super(SimplePagePlugin, self).get_response(request, page, **kwargs)

    def get_context(self, request, page, **kwargs):
        context = super(SimplePagePlugin, self).get_context(request, page, **kwargs)
        placeholder = page.placeholder_set.filter(slot='main')[0]
        if placeholder:
            datamart_items = DataMartItem.objects.filter(placeholder_id=placeholder.id)
            terms = set()
            for datamart_item in datamart_items:
                if not datamart_item.not_use_for_template_calculate:
                    datamarts_terms = datamart_item.datamarts.distinct().values_list('terms__id', flat=True)
                    datamart_item_terms = datamart_item.terms.values_list('id', flat=True)
                    terms.update(datamarts_terms)
                    terms.update(datamart_item_terms)
            context.update(
                {
                    'terms_ids': list(terms)
                }
            )

        return context
