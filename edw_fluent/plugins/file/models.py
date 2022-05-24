# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from six import python_2_unicode_compatible
from future.builtins import str

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fluent_contents.models.db import ContentItem

from edw_fluent.plugins.file import appsettings


@python_2_unicode_compatible
class FileItem(ContentItem):
    """
    RUS: Класс экземпляра файла FileItem.
    """
    file = models.FileField(
        _("file"),
        upload_to=appsettings.FILE_UPLOAD_TO
    )
    name = models.TextField(
        _("name"),
        null=True,
        blank=True
    )

    target = models.CharField(
        _("target"),
        blank=True,
        max_length=100,
        choices=((
            ("", _("same window")),
            ("_blank", _("new window")),
            ("_parent", _("parent window")),
            ("_top", _("topmost frame")),
        )),
        default=''
    )

    class Meta:
        """
        RUS: Метаданные класса FileItem.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        """
        RUS: Если нет имени, возвращает в строковом формате базовое имя пути файла.
        """
        if self.name:
            return self.name
        elif self.file:
            return str(os.path.basename(self.file.name))
        return "<empty>"
