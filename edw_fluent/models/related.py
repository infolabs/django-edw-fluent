# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from edw.models.related.entity_image import BaseEntityImage
from edw.models.related.entity_file import BaseEntityFile


# =========================================================================================================
# Entity image model
# =========================================================================================================
@python_2_unicode_compatible
class EntityImage(BaseEntityImage):
    """
    RUS: Материализованная связь многие-ко-многим с изображениями.
    """
    THUMBNAIL_KEY = 0

    key = models.IntegerField(verbose_name=_('Key'), blank=True, null=True, db_index=True)

    """Materialize many-to-many relation with images"""
    class Meta(BaseEntityImage.Meta):
        """
        RUS: Метаданные класса.
        """
        abstract = False

    def __str__(self):
        """
        RUS: Строковое представление данных.
        """
        return "{}".format(self.image)


# =========================================================================================================
# Entity image model
# =========================================================================================================
@python_2_unicode_compatible
class EntityFile(BaseEntityFile):
    """
    ENG: Materialize many-to-many relation with files.
    RUS: Материализованная связь многие-ко многим с документами.
    """
    key = models.IntegerField(verbose_name=_('Key'), blank=True, null=True, db_index=True)

    """Materialize"""
    class Meta(BaseEntityFile.Meta):
        """
        RUS: Метаданные класса.
        """
        abstract = False

    def __str__(self):
        """
        RUS: Строковое представление данных.
        """
        return "{}".format(self.file)
