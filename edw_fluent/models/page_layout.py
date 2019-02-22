# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.utils.translation import ugettext_lazy as _

from fluent_pages.models.db import PageLayout

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


#===================================================================================================================
# Возвращаем имя синонима для термина представления внешней модели
#===================================================================================================================
def get_layout_slug_by_model_name(model_name):
    return '{}-layout'.format(model_name.lower())


#===================================================================================================================
# Создаем или возвращаем корневой термин представлений
#===================================================================================================================
def get_or_create_view_layouts_root():

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


#===================================================================================================================
# Возвращаем список терминов представлений разметок страниц
#===================================================================================================================
def get_views_layouts():

    pages_views = getattr(PageLayout, VIEW_LAYOUT_CACHE_KEY, None)

    if pages_views is None:
        pages_views = {}
        try:
            root = TermModel.objects.get(
                slug=VIEW_LAYOUT_ROOT_TERM_SLUG,
                parent=None
            )
            for term in root.get_descendants(include_self=True):
                pages_views[term.slug] = term
        except TermModel.DoesNotExist:
            pass

        setattr(PageLayout, VIEW_LAYOUT_CACHE_KEY, pages_views)

    return pages_views


#==============================================================================
# Валидатор терминов для не Entity модели
#==============================================================================
def validate_term_model():

    view_root = get_or_create_view_layouts_root()

    try:  # page layout root
        layout_root = TermModel.objects.get(slug=PAGE_LAYOUT_ROOT_TERM_SLUG, parent=view_root)
    except TermModel.DoesNotExist:
        layout_root = TermModel(
            slug=PAGE_LAYOUT_ROOT_TERM_SLUG,
            parent=view_root,
            name=_('Page layout'),
            semantic_rule=TermModel.XOR_RULE,
            system_flags=_default_layout_system_flags_restriction
        )
        layout_root.save()

    for page_layout in PageLayout.objects.all():
        try:  # page layout
            TermModel.objects.get(slug=page_layout.key, parent=layout_root)
        except TermModel.DoesNotExist:
            layout = TermModel(
                slug=page_layout.key,
                parent=layout_root,
                name=page_layout.title,
                semantic_rule=TermModel.OR_RULE,
                system_flags=_default_layout_system_flags_restriction
            )
            layout.save()


#==============================================================================
# Валидатор терминов представлений для конкретной инстанции
#==============================================================================
def validate_terms(instance):
    system_flags = _default_layout_system_flags_restriction

    pages_views = get_views_layouts()

    layout_root = pages_views.get(PAGE_LAYOUT_ROOT_TERM_SLUG, None)
    if layout_root is not None:
        if instance.id is not None:
            try:
                origin = PageLayout.objects.get(pk=instance.id)
            except PageLayout.DoesNotExist:
                pass
            else:
                layout = pages_views.get(origin.key, None)
                if layout is not None:
                    layout.slug, layout.name = instance.key, instance.title
                    layout.save()
        else:
            layout = TermModel(
                slug=instance.key,
                parent=layout_root,
                name=instance.title,
                semantic_rule=TermModel.OR_RULE,
                system_flags=system_flags
            )
            layout.save()