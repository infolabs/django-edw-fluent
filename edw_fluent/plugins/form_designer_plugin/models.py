# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from form_designer.models import FormDefinition

from fluent_contents.models.db import ContentItem


@python_2_unicode_compatible
class FormDesignerItem(ContentItem):
    """
    RUS: Класс экземпляра Дизайнера форм FormDesignerItem
    """
    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE, verbose_name=_('Form'))

    def __str__(self):
        """
        RUS: Строковое представление параметра Формы.
        """
        return self.form_definition.__str__()

    class Meta:
        """
        RUS: Метаданные класса FormDesignerItem.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("Form plugin")
        verbose_name_plural = _("Form plugins")
