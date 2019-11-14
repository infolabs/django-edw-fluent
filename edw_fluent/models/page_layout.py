# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fluent_pages.models.db import PageLayout

from django.utils.translation import ugettext_lazy as _

from edw.models.term import TermModel

VIEW_LAYOUT_ROOT_TERM_SLUG = 'view-layout'
PAGE_LAYOUT_ROOT_TERM_SLUG = 'page-layout'

VIEW_LAYOUT_CACHE_KEY = '_view_layout_cache'


_default_layout_system_flags_restriction = (
    TermModel.system_flags.delete_restriction
    | TermModel.system_flags.change_parent_restriction
    | TermModel.system_flags.change_slug_restriction
    | TermModel.system_flags.change_semantic_rule_restriction
    | TermModel.system_flags.has_child_restriction
)


def get_layout_slug_by_model_name(model_name):
    """
    Возвращаем имя синонима для термина представления внешней модели
    """
    return '{}-layout'.format(model_name.lower())


def get_or_create_view_layouts_root():
    """
    Создаем или возвращаем корневой термин представлений
    """
    view_root = getattr(PageLayout, '_view_layouts_root_cache', None)

    if not view_root:
        try:  # view layout root
            view_root = TermModel.objects.get(slug=VIEW_LAYOUT_ROOT_TERM_SLUG, parent=None)
        except TermModel.DoesNotExist:
            view_root = TermModel(
                slug=VIEW_LAYOUT_ROOT_TERM_SLUG,
                parent=None,
                name=_('View'),
                semantic_rule=TermModel.XOR_RULE,
                system_flags=_default_layout_system_flags_restriction
            )
            view_root.save()

        PageLayout._view_layouts_root_cache = view_root

    return view_root


def get_views_layouts():
    """
    Возвращаем список терминов представлений разметок страниц и объектов
    """
    views_layouts = getattr(PageLayout, VIEW_LAYOUT_CACHE_KEY, None)

    if views_layouts is None:
        views_layouts = {}
        try:
            root = TermModel.objects.get(
                slug=VIEW_LAYOUT_ROOT_TERM_SLUG,
                parent=None
            )
            for term in root.get_descendants(include_self=True):
                views_layouts[term.slug] = term
        except TermModel.DoesNotExist:
            pass

        setattr(PageLayout, VIEW_LAYOUT_CACHE_KEY, views_layouts)

    return views_layouts


def validate_term_model():
    """
    Валидатор терминов для не Entity модели
    """
    views_layouts_root = get_or_create_view_layouts_root()

    try:  # page layout root
        pages_layouts_root = TermModel.objects.get(slug=PAGE_LAYOUT_ROOT_TERM_SLUG, parent=views_layouts_root)
    except TermModel.DoesNotExist:
        pages_layouts_root = TermModel(
            slug=PAGE_LAYOUT_ROOT_TERM_SLUG,
            parent=views_layouts_root,
            name=_('Page layout'),
            semantic_rule=TermModel.XOR_RULE,
            system_flags=_default_layout_system_flags_restriction
        )
        pages_layouts_root.save()

    for page_layout in PageLayout.objects.all():
        try:  # page layout
            TermModel.objects.get(slug=page_layout.key, parent=pages_layouts_root)
        except TermModel.DoesNotExist:
            layout = TermModel(
                slug=page_layout.key,
                parent=pages_layouts_root,
                name=page_layout.title,
                semantic_rule=TermModel.OR_RULE,
                system_flags=_default_layout_system_flags_restriction
            )
            layout.save()


def validate_terms(instance):
    """
    Валидатор терминов представлений для конкретной инстанции
    """
    system_flags = _default_layout_system_flags_restriction

    views_layouts = get_views_layouts()

    pages_layouts_root = views_layouts.get(PAGE_LAYOUT_ROOT_TERM_SLUG, None)
    if pages_layouts_root is not None:
        if instance.id is not None:
            try:
                origin = PageLayout.objects.get(pk=instance.id)
            except PageLayout.DoesNotExist:
                pass
            else:
                layout = pages_layouts_root.get(origin.key, None)
                if layout is not None:
                    layout.slug, layout.name = instance.key, instance.title
                    layout.save()
        else:
            layout = TermModel(
                slug=instance.key,
                parent=pages_layouts_root,
                name=instance.title,
                semantic_rule=TermModel.OR_RULE,
                system_flags=system_flags
            )
            layout.save()
