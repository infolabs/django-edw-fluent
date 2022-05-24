# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six import with_metaclass, python_2_unicode_compatible

from filer.fields.image import FilerImageField

from django.db import models
from django.utils.translation import ugettext_lazy as _

from edw import deferred
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


# =========================================================================================================
# BaseEntityComment
# =========================================================================================================
@python_2_unicode_compatible
class BaseEntityComment(with_metaclass(deferred.ForeignKeyBuilder, models.Model)):
    """
    Comment model
    """
    entity = deferred.ForeignKey('BaseEntity', on_delete=models.CASCADE, verbose_name=_('Entity'))

    origin_name = models.CharField(
        verbose_name=_('Origin name'),
        help_text=_('Comment owner name. You must indicate the source of comment (company name/full name '
                    'and position of the company representative)'),
        blank=False,
        null=False,
        max_length=255
    )
    text = models.TextField(
        verbose_name=_('Text'),
        help_text=_('Text of comment, contains a quote with a rebuttal (maximum 300 symbols).'),
        blank=False,
        null=False,
        max_length=300
    )
    origin_url = models.CharField(
        verbose_name=_('Origin url'),
        help_text=_('Comment owner link, refers to materials containing a denial on the media website.'),
        blank=True,
        null=True,
        max_length=255
    )
    logo = FilerImageField(
        on_delete=models.CASCADE,
        verbose_name=_('Origin logo'),
        help_text=_('Comment owner logo'),
        blank=True,
        null=True,
    )
    bind_to = models.TextField(
        verbose_name=_('Bind to'),
        help_text=_('Refers to a news item that has been commented on. If the news has been published by several '
                    'media outlets, you can post links to each source. Including yourself. Separate by newline'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
        verbose_name = _("Publication comment")
        verbose_name_plural = _("Publication comments")

    def __str__(self):
        return "{} ({})".format(self.origin_name, self.origin_url)

# =========================================================================================================
# PublicationComment for materialize
# =========================================================================================================
class PublicationComment(BaseEntityComment):

    key = models.IntegerField(
        verbose_name=_('Key'),
        blank=True,
        null=True,
        db_index=True
    )

    class Meta(BaseEntityComment.Meta):
        """
        RUS: Метаданные класса.
        """
        abstract = False

    @property
    def _bind_to(self):
        return self.bind_to.splitlines()
