# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from edw.models.entity import EntityModel


# =========================================================================================================
# BaseTemplate
# =========================================================================================================
class BaseTemplate(EntityModel.materialized):
    """
    RUS: Класс базового шаблона.
    Определяет поля и их значения (Имя, На индексации), способ сортировки.
    """
    ORDER_BY_NAME_ASC = 'basetemplate__name'

    ORDERING_MODES = (
        (ORDER_BY_NAME_ASC, _('Alphabetical')),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        blank=False,
        null=False,
        default=''
    )
    index = models.CharField(
        max_length=255,
        verbose_name=_("On indexation"),
        blank=False,
        null=False,
        db_index=True,
        default=''
    )

    class Meta:
        """
        RUS: Метаданные класса.
        """
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    class RESTMeta:
        """
        RUS: Метаданные класса для REST-сериалайзера.
        """
        exclude = ['images']

    @property
    def entity_name(self):
        """
        RUS: Возвращает имя сущности.
        """
        return self.name

    def get_template(self):
        """
        RUS: Загружает шаблон с именем 'template' и возвращает объект Template.
        """
        return getattr(self, 'template', None)

    def pre_save_entity(self, origin, *args, **kwargs):
        """
        RUS: Функция вызывается перед методом Сохранить.
        Определяет условия загрузки шаблонов и путь к ним.
        """
        super(BaseTemplate, self).pre_save_entity(origin, *args, **kwargs)

        templates = self.get_template().get_templates()
        self.index = " ".join(templates)
