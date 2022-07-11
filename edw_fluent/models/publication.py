# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from operator import or_
from functools import reduce
from fluent_contents.models import Placeholder


from django.conf import settings
from django.db import models
from django.db.models import ExpressionWrapper, F, Q, Case, When
from django.core.exceptions import ValidationError
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from fluent_contents.models import PlaceholderField, ContentItemRelation
from chakert import Typograph

from edw.models.entity import EntityModel, BaseEntityManager, BaseEntityQuerySet
from edw.models.term import TermModel
from edw.utils.dateutils import datetime_to_local

from edw_fluent.models.page_layout import (
    get_views_layouts,
    get_layout_slug_by_model_name,
    get_or_create_view_layouts_root
)
from edw_fluent.models.mixins import ImagesFilesFluentMixin, CommentsFluentMixin
from edw_fluent.models.related.entity_related_data_mart import EntityRelatedDataMart
from edw_fluent.plugins.block.models import BlockItem

_publication_root_terms_system_flags_restriction = (
    TermModel.system_flags.delete_restriction
    | TermModel.system_flags.change_parent_restriction
    | TermModel.system_flags.change_slug_restriction
)


# =========================================================================================================
# PublicationBase queryset
# =========================================================================================================
class PublicationBaseQuerySet(BaseEntityQuerySet):

    def published(self):
        raise NotImplementedError(
            '{cls}.published() must be implemented.'.format(
                cls=self.__class__.__name__
            )
        )


# =========================================================================================================
# PublicationBase manager
# =========================================================================================================
PublicationBaseManager = BaseEntityManager.from_queryset(PublicationBaseQuerySet)

# =========================================================================================================
# PublicationBase model
# =========================================================================================================
class PublicationBase(EntityModel.materialized, ImagesFilesFluentMixin, CommentsFluentMixin):
    """
    RUS: Базовая модель публикаций.
    Определяет поля и их значения, компоненты представления, способы сортировки.
    """
    ORDER_BY_NAME_ASC = 'publication__title'
    ORDER_BY_DATE = '-publication__created_at'
    ORDER_BY_CHRONOLOGICAL = "-publication__chronological"
    ORDER_BY_RECOMMENDATION = "-publication__pinned,-publication__created_at"

    ORDERING_MODES = (
        (ORDER_BY_DATE, _('By date')),
        (ORDER_BY_CHRONOLOGICAL, _('By chronology')),
        (ORDER_BY_RECOMMENDATION, _('By recommendation')),
        (ORDER_BY_NAME_ASC, _('Alphabetical')),
    )

    VIEW_COMPONENT_TILE = 'publication_tile'
    VIEW_COMPONENT_LIST = 'publication_list'
    VIEW_COMPONENT_TABLE = 'publication_table'

    VIEW_COMPONENTS = (
        (VIEW_COMPONENT_TILE, _('Publication tile')),
        (VIEW_COMPONENT_LIST, _('Publication list')),
        (VIEW_COMPONENT_TABLE, _('Publication table')),
    )

    LAYOUT_TERM_SLUG = get_layout_slug_by_model_name('publication')

    SHORT_SUBTITLE_MAX_WORDS_COUNT = 17
    SHORT_SUBTITLE_MAX_CHARS_COUNT = 145
    SHORT_SUBTITLE_TRUNCATE = '...'

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        blank=False,
        null=False,
    )

    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=255,
        blank=True,
        null=True,
        default=''
    )

    lead = models.TextField(
        verbose_name=_("Lead"),
        blank=False,
        null=False
    )

    tags = models.CharField(
        verbose_name=_('tags'),
        help_text=_('Use semicolon as tag divider'),
        max_length=255,
        blank=True,
        db_index=True
    )

    statistic = models.IntegerField(
        verbose_name=_("Statistic"),
        blank=False,
        default='0'
    )

    pinned = models.BooleanField(
        verbose_name=_("Is main publication"),
        default=False
    )

    content = PlaceholderField(
        "content",
        verbose_name=_("Content")
    )

    contentitem_set = ContentItemRelation()

    unpublish_at = models.DateTimeField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name=_('Unpublish at'),
    )

    objects = PublicationBaseManager()

    class Meta:
        """
        RUS: Метаданные класса.
        """
        abstract = True
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")

    class RESTMeta:
        """
        RUS: Метакласс для определения параметров сериалайзера.
        """
        include = {
            'detail_url': ('rest_framework.serializers.CharField', {
                'source': 'get_detail_url',
                'read_only': True
            }),
            'terms_ids': ('rest_framework.serializers.ListField', {
                'child': serializers.IntegerField(),
                'source': 'active_terms_ids'
            }),
            'placeholder_id': ('rest_framework.serializers.IntegerField', {
                'source': 'get_placeholder',
                'read_only': True
            }),
            'default_data_mart': ('edw.rest.serializers.entity.RelatedDataMartSerializer', {
                'source': 'data_mart',
                'read_only': True
            }),
            'defaults_data_marts': ('edw.rest.serializers.entity.RelatedDataMartSerializer', {
                'read_only': True,
                'many': True
            }),
            'blocks_count': ('rest_framework.serializers.IntegerField', {
                'read_only': True
            }),
            'related_by_tags': ('edw.rest.serializers.entity.EntitySummarySerializer', {
                'source': 'get_related_by_tags_publications',
                'read_only': True,
                'many': True
            }),
            'gallery': ('edw.rest.serializers.related.entity_image.EntityImageSerializer', {
                'read_only': True,
                'many': True
            }),
            'thumbnail': ('edw.rest.serializers.related.entity_image.EntityImageSerializer', {
                'read_only': True,
                'many': True
            }),
            'attachments': ('edw.rest.serializers.related.entity_file.EntityFileSerializer', {
                'read_only': True,
                'many': True
            }),
            'default_comments': ('edw_fluent.rest.serializers.comment.PublicationCommentSerializer', {
                'read_only': True,
                'many': True
            }),
            # todo: здесь сериализуются все комментарии, а не только комментарий по умолчанию. рескомментировать, если
            #  в будущем понадобится, пока нет смысла, поскольку комментарии привязанные к блокам передаются в рендер блока
            #  непосредственно в контекст, а для получения этих данных в rss есть метод инстанции get_ordered_comments()
            # 'ordered_comments': ('edw_fluent.rest.serializers.comment.PublicationCommentSerializer', {
            #     'read_only': True,
            #     'many': True
            # }),
            'created_at': ('rest_framework.serializers.DateTimeField', {
                'source': 'local_created_at',
                'read_only': True
            }),
            'short_subtitle': ('rest_framework.serializers.CharField', {
                'source': 'get_short_subtitle',
                'read_only': True
            }),
        }

        exclude = ['images', 'files', 'stored_request']

        filters = {
            # Tags: см. пример в описании фильтра
            'tags': ("edw_fluent.rest.filters.publication.TagFilter", {
                'name': 'publication__tags'
            }),
            'q': ("rest_framework_filters.CharFilter", {
                'name': 'publication__title',
                'lookup_expr': 'icontains',
            })
        }

    def __str__(self):
        """
        RUS: Переопределяет заголовок в строковом формате.
        """
        return self.title

    @property
    def entity_name(self):
        """
        RUS: Возвращает переопределенный заголовок.
        """
        return self.title

    @classmethod
    def get_ordering_modes(cls, **kwargs):
        """
        RUS: Возвращает отсортированные модели, являющиеся методами класса.
        """
        full = cls.ORDERING_MODES

        context = kwargs.get("context", None)
        if context is None:
            return full
        ordering = context.get('ordering', None)
        if not ordering:
            return full

        ordering = ordering[0]

        created = '-publication__created_at'
        chrono = '-publication__chronological'

        mode_to_remove = None
        if ordering == created:
            mode_to_remove = chrono
        elif ordering == chrono:
            mode_to_remove = created

        return [m for m in full if m[0] != mode_to_remove]

    @classmethod
    def get_summary_annotation(cls, request):
        """
        RUS: Возвращает аннотированные данные для сводного сериалайзера.
        """
        return {
            'publication__chronological': (
                Case(
                    When(
                        publication__pinned=True,
                        then=ExpressionWrapper(F('created_at') + datetime.timedelta(days=1),
                                               output_field=models.DateTimeField())
                    ),
                    default=F('created_at'),
                ),
            ),
        }

    @property
    def local_created_at(self):
        """
        Преобразовывает дату/время создания объекта в формат даты/времени с учетом таймзоны заданой в настройках.
        В базе данных дата/время сохраняется в формате UTC и при сериализации в результате не будет указано смещение
        и для использования в шаблонах и внешних системах надо будет каким-то образом задавать смещение времени, для
        упрощения работы с сериализованными данными это преобразование нужно сделать на этапе сериализации.
        В конкретных моделях данных надо в сериалайзере использовать данный метод в качестве источника данных (src).
        Например:
            2019-11-13T12:15:04.748250Z - сериализованные данные до преобразования
            2019-11-13T15:15:04+03:00 - сериализованные данные после преобразования
        :return: дата/время в нужной таймзоне
        """
        return datetime_to_local(self.created_at)

    def get_updated_at(self):
        """
        Преобразовывает дату/время обновления объекта в формат даты/времени с учетом таймзоны заданой в настройках.
        В базе данных дата/время сохраняется в формате UTC и при сериализации в результате не будет указано смещение
        и для использования в шаблонах и внешних системах надо будет каким-то образом задавать смещение времени, для
        упрощения работы с сериализованными данными это преобразование нужно сделать на этапе сериализации.
        В конкретных моделях данных надо в сериалайзере использовать данный метод в качестве источника данных (src).
        Например:
            2019-11-13T12:15:04.748250Z - сериализованные данные до преобразования
            2019-11-13T15:15:04+03:00 - сериализованные данные после преобразования
        :return: дата/время в нужной таймзоне
        """
        return datetime_to_local(self.updated_at)

    def clean(self, *args, **kwargs):
        """
        RUS: Меняет шрифт текста в заголовке, подзаголовке, ЛИДе на шрифт Typograph.
        Ограничивает количество символов в заголовке до 90 знаков.
        """
        self.title = Typograph.typograph_text(self.title, 'ru')
        if self.subtitle:
            self.subtitle = Typograph.typograph_text(self.subtitle, 'ru')
        if self.lead:
            self.lead = Typograph.typograph_text(self.lead, 'ru')
        max_length  = getattr(settings, 'PUBLICATION_TITLE_MAX_LENGTH', 90)
        len_title = len(self.title)
        if len_title > max_length:
            raise ValidationError(_('The maximum number of characters {}, you have {}').format(max_length, len_title))

    def get_placeholder(self):
        """
        RUS: Возвращает id контента.
        """
        return self.content.id

    @cached_property
    def breadcrumbs(self):
        """
        RUS: Возвращает хлебные крошки, если есть витрина данных и страница к ней.
        """
        data_mart = self.data_mart

        if data_mart:
            page = data_mart.get_detail_page()
            if page:
                return page.breadcrumb

        return None

    @cached_property
    def blocks_count(self):
        """
        RUS: Получает количество текстовых блоков публикации.
        """
        return self.get_blocks_count()

    def get_blocks_count(self):
        """
        RUS: В соответствии с количеством и номером текстового блока формирует страницу.
        """
        return BlockItem.objects.filter(placeholder=self.content).count()

    def get_short_subtitle(self):
        """
        RUS: Подзаголовок берется из заполненного соответствующего поля, при его отсутствии берется из ЛИД.
        При превышении длины подзаголовок обрезается до нужного количества символов.
        """
        value = self.subtitle if self.subtitle else self.lead
        return Truncator(
            Truncator(value).words(self.SHORT_SUBTITLE_MAX_WORDS_COUNT,
                                   truncate=self.SHORT_SUBTITLE_TRUNCATE, html=True)
        ).chars(self.SHORT_SUBTITLE_MAX_CHARS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE, html=True)

    @cached_property
    def short_subtitle(self):
        """
        RUS: Возвращает подзаголовок соответствующего размера.
        """
        return self.get_short_subtitle()

    def get_summary_extra(self, context):
        """
        ENG: Return extra data for summary serializer.
        RUS: Возвращает дополнительные данные для сводного сериалайзера.
        """
        data_mart = context.get('data_mart', None)
        extra = {
            'url': self.get_detail_url(data_mart),
            'created_at': self.local_created_at,
            'updated_at': self.updated_at,
            'statistic': self.statistic,
            'short_subtitle': self.short_subtitle,
        }
        return extra

    def get_detail_url(self, data_mart=None):
        """
        RUS: Возвращает конечный url публикации.
        Получает адрес страницы публикации.
        """
        if data_mart is None:
            data_mart = self.data_mart
        if data_mart:
            page = data_mart.get_detail_page()
            return reverse('publication_detail', args=[page.url.strip('/'), self.pk] if page is not None else [self.pk])
        else:
            return reverse('publication_detail', args=[self.pk])

    def get_tags(self):
        if self.tags and self.tags.strip():
            tags = [tag.strip() for tag in self.tags.split(';')]
            tags = [tag for tag in tags if tag]
            return tags
        else:
            return []

    @cached_property
    def text_blocks(self):
        """
        RUS: Возвращает список текстовых блоков.
        """
        return list(self.content.contentitems.instance_of(BlockItem))

    def get_related_by_tags_publications(self, exclude_blockitem=True):
        """
        Вернуть публикации, имеющие общие тэги с текущей публикацией
        """
        exclude_ids = list(
            self.content.contentitems.instance_of(BlockItem).exclude(
                blockitem__subjects__isnull=True).values_list('blockitem__subjects__id', flat=True)
        ) if exclude_blockitem else []

        exclude_ids.append(self.id)
        if not hasattr(self, '_Publication__related_publications_cache'):
            tags = self.get_tags()
            if tags:
                related_by_tags_count = getattr(settings, 'RELATED_BY_TAGS_COUNT', 5)
                self.__related_publications_cache = EntityModel.objects \
                    .active() \
                    .exclude(pk__in=exclude_ids) \
                    .filter(reduce(
                        or_, [Q(publication__tags__icontains=tag) for tag in tags]
                    )) \
                    .order_by('-created_at')[:related_by_tags_count]
            else:
                self.__related_publications_cache = self.__class__.objects.none()

        return self.__related_publications_cache

    def defaults_data_marts(self):
        return [x.data_mart for x in EntityRelatedDataMart.objects.filter(key=None, entity=self)]

    @classmethod
    def get_view_components(cls, **kwargs):
        """
        RUS: Возвращает view components (компоненты представлений): плиточное представление, список.
        """
        full = cls.VIEW_COMPONENTS
        if hasattr(cls, 'VIEW_COMPONENT_MAP'):
            reduced = tuple([c for c in full if c[0] != cls.VIEW_COMPONENT_MAP])

            context = kwargs.get("context", None)
            if context is None:
                return reduced

            term_ids = context.get('real_terms_ids', None)
            if not term_ids:
                return reduced

        return full

    def get_or_create_placeholder(self):
        try:
            placeholder = Placeholder.objects.get_by_slot(self, "content")
        except Placeholder.DoesNotExist:
            placeholder = Placeholder.objects.create_for_object(self, "content")

        return placeholder

    @classmethod
    def validate_term_model(cls):
        """
        RUS: Валидация модели терминов.
        Добавляет термины класса объекта в дерево согласно структуре наследования.
        """
        view_root = get_or_create_view_layouts_root()
        try:  # publication root
            TermModel.objects.get(slug=cls.LAYOUT_TERM_SLUG, parent=view_root)
        except TermModel.DoesNotExist:
            publication_root = TermModel(
                slug=cls.LAYOUT_TERM_SLUG,
                parent=view_root,
                name=_('Publication'),
                semantic_rule=TermModel.XOR_RULE,
                system_flags=_publication_root_terms_system_flags_restriction
            )
            publication_root.save()

        super(PublicationBase, cls).validate_term_model()

    def need_terms_validation_after_save(self, origin, **kwargs):
        """
        RUS: Проставляет автоматически термины, связанные с макетом представления публикации,
        после ее сохранения.
        """
        do_validate_layout = kwargs["context"]["validate_view_layout"] = True
        return super(PublicationBase, self).need_terms_validation_after_save(
            origin, **kwargs) or do_validate_layout

    def validate_terms(self, origin, **kwargs):
        """
        RUS: При выборе макета представления и его сохранения, проставляются соответствующие термины и выбирается
        автоматически соответствующий шаблон.
        При изменении макета, термины удаляются и заменяются новыми, соответствующими новому макету.
        """
        context = kwargs["context"]

        force_validate_terms = context.get("force_validate_terms", False)

        if force_validate_terms or context.get("validate_view_layout", False):
            views_layouts = get_views_layouts()
            to_remove = [v for k, v in views_layouts.items() if k != PublicationBase.LAYOUT_TERM_SLUG]
            self.terms.remove(*to_remove)
            to_add = views_layouts.get(PublicationBase.LAYOUT_TERM_SLUG, None)
            if to_add is not None:
                self.terms.add(to_add)
        super(PublicationBase, self).validate_terms(origin, **kwargs)
