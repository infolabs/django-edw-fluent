# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import decorator_from_middleware_with_args

from django.utils.cache import (
    get_max_age, has_vary_header, learn_cache_key as origin_learn_cache_key,
    patch_response_headers,
)

from fluent_pages.models import PageLayout
from fluent_pages.integration.fluent_contents.models import FluentContentsPage

from edw.utils.circular_buffer_in_cache import RingBuffer


db_table_name_pattern = '{}_{}'.format(settings.EDW_APP_LABEL, '{}')

# =========================================================================================================
# Catch Simple Page cache key
# =========================================================================================================
SIMPLE_PAGE_BUFFER_CACHE_KEY = 'spg_bf'
SIMPLE_PAGE_BUFFER_CACHE_SIZE = getattr(settings, 'SIMPLE_PAGE_BUFFER_CACHE_SIZE', 100)


def get_simple_page_buffer():
    """
    RUS: Собирает кольцевой буфер SimplePage с ключом кэша и указанием максимального размера.
    """
    return RingBuffer.factory(SIMPLE_PAGE_BUFFER_CACHE_KEY,
                              max_size=SIMPLE_PAGE_BUFFER_CACHE_SIZE)


def clear_simple_page_buffer():
    """
    RUS: Очищает буфер, удаляя по указанным ключам.
    """
    buf = get_simple_page_buffer()
    keys = buf.get_all()
    buf.clear()
    cache.delete_many(keys)


# Monkey path: save cache_key for invalidation
def learn_cache_key(request, response, timeout, key_prefix, cache):
    """
    RUS: Сохраняет ключ кэша для инвалидации, удаляет старый кэш по ключу,
    если он не является акутуальным.
    """
    cache_key = origin_learn_cache_key(request, response, timeout, key_prefix, cache)

    # reduce cache
    buf = get_simple_page_buffer()
    old_key = buf.record(cache_key)
    if old_key != buf.empty:
        cache.delete(old_key)

    return cache_key


class SimplePageCacheMiddleware(CacheMiddleware):
    """
    RUS: Узнает, какие заголовки следует учитывать для пути запроса от объекта ответа.
    Сохраняет ключ кэша (не кэширует заново), если он тождественен оригинальному в следующих случаях:
    """
    # path `learn_cache_key`, method code equal with origin
    def process_response(self, request, response):
        """
        RUS: Возвращает ответ сервера, если пользователь идентифицирован.
        """
        if request.user.is_authenticated():
            return response

        """Sets the cache, if needed."""
        if not self._should_update_cache(request, response):
            return response
        # RUS: Возвращает ответ сервера, если не было обновления кэша.

        if response.streaming or response.status_code != 200:
            return response
        # RUS: Возвращает ответ сервера, если, у атрибута HttpResponse.streaming статус False
        # или код ответа не равен 200.

        # Не кэширует ответы сервера, которые устанавливают специфичные для пользователя (и, возможно,
        # чувствительные к безопасности ) cookie в ответ на запрос без cookie
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
        # Возвращает максимальный возраст из заголовка Cache-Control ответа в виде целого числа (
        # Пытается получить время хранения кэша из заголовка Cache-Control.
        # При его отсутствии, время хранения кэша равно значению по умолчанию,
        # если же установлено равным 0, возвращается некэшированный ответ сервера

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
        # RUS: Добавляет заголовки (ответ сервера, время хранения кэша) к объекту HttpResponse при кэшиировании.
        # Если время хранения кэша истекло, добавляется обратный вызов, который будет вызван после рендеринга,
        # иначе в кэш будут добавлены (ключ кэша, ответ сервера, время хранения кэша).

    def process_request(self, request):
        # Don't cache responses that set a user-specific
        # RUS: Не кэширует ответ сервера от пользователей, прошедших идентификацию.
        if request.user.is_authenticated():
            return None
        else:
            return super(SimplePageCacheMiddleware, self).process_request(request)

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
    # RUS: Декоратор для представлений, который пытается получить страницу из кэша
    # и  заполняет кэш, если страницы еще нет в кэше.
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
    """
    RUS: Класс для создания страниц.
    Опеределяет поля (Макет, SEO-заголовок) и их характеристики.
    """
    layout = models.ForeignKey(
        PageLayout,
        verbose_name=_('Layout'),
        null=True,
    )
    seo_title = models.CharField(
        verbose_name=_('SEO title'),
        max_length=255,
        null=True,
        blank=True,
    )

    terms = models.ManyToManyField(
        'Term',
        related_name='page_terms',
        db_table=db_table_name_pattern.format('page_terms')
    )

    class Meta:
        """
        RUS: Метаданные класса.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("Simple page")
        verbose_name_plural = _("Simple pages")
        permissions = (
            ('change_page_layout', _("Can change Page layout")),
        )