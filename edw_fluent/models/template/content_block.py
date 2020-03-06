# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from page_builder.fields import BuilderTemplateField

from edw_fluent.models.page_layout import get_views_layouts

from edw_fluent.models.template.base import BaseTemplate
from edw_fluent.models.page_builder import get_page_builder_elements_by_model

from edw_fluent.models.publication import PublicationBase


# =========================================================================================================
# ContentBlockTemplate
# =========================================================================================================
class ContentBlockTemplate(BaseTemplate):
    """
    RUS: Класс Шаблон контент-блока.
    Определяет поля и их значения (Имя, На индексации), способ сортировки.
    """
    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        elements=get_page_builder_elements_by_model('ContentBlockTemplate'),
        help_text=_("Some help text about content block template... `index`, `top`, `bottom`...")
    )

    class Meta:
        """
        RUS: Метаданные класса ContentBlockTemplate.
        """
        verbose_name = _("Content Block Template")
        verbose_name_plural = _("Content Block Templates")

    def need_terms_validation_after_save(self, origin, **kwargs):
        """
        RUS: Проставляет автоматически термины, связанные с шаблоном контент-блока,
        после ее сохранения.
        """
        do_validate = kwargs["context"]["validate_view_layout"] = True
        return super(ContentBlockTemplate, self).need_terms_validation_after_save(
            origin, **kwargs) or do_validate

    def validate_terms(self, origin, **kwargs):
        """
        RUS: При выборе шаблона контент-блока и его сохранения, проставляются соответствующие термины и выбирается
        автоматически соответствующий шаблон.
        При изменении шаблона контент-блока, термины удаляются и заменяются новыми, соответствующими новому шаблону.
        """
        context = kwargs["context"]
        if context.get("force_validate_terms", False) or context.get("validate_view_layout", False):
            views_layouts = get_views_layouts()
            to_remove = [v for k, v in views_layouts.items() if k != PublicationBase.LAYOUT_TERM_SLUG]
            self.terms.remove(*to_remove)
            to_add = views_layouts.get(PublicationBase.LAYOUT_TERM_SLUG, None)
            if to_add is not None:
                self.terms.add(to_add)

        super(ContentBlockTemplate, self).validate_terms(origin, **kwargs)
