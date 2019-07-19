# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.models import ExpressionWrapper, F, Case, When
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from fluent_contents.models import PlaceholderField, ContentItemRelation
from chakert import Typograph

from edw.models.entity import EntityModel
from edw.models.term import TermModel

from edw_fluent.models.related import EntityImage, EntityFile
from edw_fluent.models.page_layout import (
    get_views_layouts,
    get_layout_slug_by_model_name,
    get_or_create_view_layouts_root
)
from edw_fluent.plugins.block.models import BlockItem

_publication_root_terms_system_flags_restriction = (
    TermModel.system_flags.delete_restriction
    | TermModel.system_flags.change_parent_restriction
    | TermModel.system_flags.change_slug_restriction
)


def naive_date_to_utc_date(naive_date):
    return naive_date \
        .replace(tzinfo=timezone.utc) \
        .astimezone(tz=timezone.get_current_timezone()) \
        .replace(tzinfo=timezone.utc)


# =========================================================================================================
# PublicationBase model
# =========================================================================================================
class PublicationBase(EntityModel.materialized):

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

    VIEW_COMPONENTS = (
        (VIEW_COMPONENT_TILE, _('Publication tile')),
        (VIEW_COMPONENT_LIST, _('Publication list')),
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

    TRANSITION_TARGETS = {
        'draft': _("Publication draft"),
        'on_editing': _("Publication on editing"),
        'on_approval': _("Publication on approval"),
        'published': _("Published")
    }

    class Meta:
        abstract = True
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")

    class RESTMeta:
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
            'blocks_count': ('rest_framework.serializers.IntegerField', {
                'read_only': True
            }),
            'related_by_tags': ('edw.rest.serializers.entity.EntityDetailSerializer', {
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
            'created_at': ('rest_framework.serializers.DateTimeField', {
                'source': 'get_created_at',
                'read_only': True
            }),
            'short_subtitle': ('rest_framework.serializers.CharField', {
                'source': 'get_short_subtitle',
                'read_only': True
            }),
        }
        exclude = ['images', 'files', 'stored_request']

    def __str__(self):
        return self.title

    @property
    def entity_name(self):
        return self.title

    # todo: NOT WORK! RECURSION
    # @classmethod
    # def get_ordering_modes(cls, **kwargs):
    #     full = super(EntityModel.materialized, cls).get_ordering_modes(**kwargs)
    #
    #     context = kwargs.get("context", None)
    #     if context is None:
    #         return full
    #     ordering = context.get('ordering', None)
    #     if not ordering:
    #         return full
    #
    #     ordering = ordering[0]
    #
    #     created = '-publication__created_at'
    #     chrono = '-publication__chronological'
    #
    #     mode_to_remove = None
    #     if ordering == created:
    #         mode_to_remove = chrono
    #     elif ordering == chrono:
    #         mode_to_remove = created
    #
    #     return [m for m in full if m[0] != mode_to_remove]

    @classmethod
    def get_summary_annotation(cls):
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

    def get_created_at(self):
        return naive_date_to_utc_date(self.created_at)

    def get_updated_at(self):
        return naive_date_to_utc_date(self.updated_at)

    def clean(self, *args, **kwargs):
        self.title = Typograph.typograph_text(self.title, 'ru')
        self.subtitle = Typograph.typograph_text(self.subtitle, 'ru')
        self.lead = Typograph.typograph_text(self.lead, 'ru')

        len_title = len(self.title)
        if len_title > 90:
            raise ValidationError(_('The maximum number of characters 90, you have {}').format(len_title))

    def get_placeholder(self):
        return self.content.id

    @cached_property
    def ordered_images(self):
        return list(self.get_ordered_images())

    @cached_property
    def breadcrumbs(self):
        data_mart = self.data_mart

        if data_mart:
            page = data_mart.get_detail_page()
            if page:
                return page.breadcrumb

        return None

    def get_ordered_images(self):
        return self.images.all().order_by('entityimage__order')

    @cached_property
    def blocks_count(self):
        return self.get_blocks_count()

    def get_blocks_count(self):
        return BlockItem.objects.filter(placeholder=self.content).count()

    @cached_property
    def gallery(self):
        return list(self.get_gallery())

    def get_gallery(self):
        return EntityImage.objects.filter(entity=self, key=None).select_related('image').order_by('order')

    @cached_property
    def thumbnail(self):
        return list(self.get_thumbnail())

    def get_thumbnail(self):
        return EntityImage.objects.filter(entity=self, key=EntityImage.THUMBNAIL_KEY).order_by('order')

    @cached_property
    def attachments(self):
        return list(self.get_attachments())

    def get_attachments(self):
        return EntityFile.objects.filter(entity=self, key=None).order_by('order')

    @cached_property
    def thumbnails(self):
        thumbnails = [x.image for x in
                      EntityImage.objects.filter(entity=self, key=EntityImage.THUMBNAIL_KEY).order_by('order')]
        if thumbnails:
            return thumbnails
        else:
            thumbnails = [x.image for x in self.gallery]
            if thumbnails:
                return thumbnails[:1]
            else:
                return self.ordered_images[:1]

    def get_short_subtitle(self):
        value = self.subtitle if self.subtitle else self.lead
        return Truncator(
            Truncator(value).words(self.SHORT_SUBTITLE_MAX_WORDS_COUNT,
                                   truncate=self.SHORT_SUBTITLE_TRUNCATE, html=True)
        ).chars(self.SHORT_SUBTITLE_MAX_CHARS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE, html=True)

    @cached_property
    def short_subtitle(self):
        return self.get_short_subtitle()

    def get_summary_extra(self, context):
        data_mart = context['data_mart']
        extra = {
            'url': self.get_detail_url(data_mart),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'statistic': self.statistic,
            'short_subtitle': self.short_subtitle,
        }
        return extra

    def get_detail_url(self, data_mart=None):
        if data_mart is None:
            data_mart = self.data_mart
        if data_mart:
            page = data_mart.get_detail_page()
            return reverse('publication_detail', args=[page.url.strip('/'), self.pk] if page is not None else [self.pk])
        else:
            return reverse('publication_detail', args=[self.pk])

    @cached_property
    def text_blocks(self):
        return list(self.content.contentitems.instance_of(BlockItem))

    @classmethod
    def _get_root_term(cls, cache_key, slug):
        """Получить корневой термин по слагу, сохранить его в атрибут класса"""
        if not hasattr(cls, cache_key):
            root_term = TermModel.objects.get(
                slug=slug,
                parent=None,
            )
            setattr(cls, cache_key, root_term)
        return getattr(cls, cache_key)

    # todo: NOT WORK! RECURSION
    # @classmethod
    # def get_view_components(cls, **kwargs):
    #     full = super(PublicationBase, cls).get_view_components(**kwargs)
    #     reduced = tuple([c for c in full if c[0] != cls.VIEW_COMPONENT_MAP])
    #
    #     context = kwargs.get("context", None)
    #     if context is None:
    #         return reduced
    #
    #     term_ids = context.get('real_terms_ids', None)
    #     if not term_ids:
    #         return reduced
    #
    #     return full

    @classmethod
    def validate_term_model(cls):
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
        do_validate_layout = kwargs["context"]["validate_view_layout"] = True
        return super(PublicationBase, self).need_terms_validation_after_save(
            origin, **kwargs) or do_validate_layout

    def validate_terms(self, origin, **kwargs):
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
