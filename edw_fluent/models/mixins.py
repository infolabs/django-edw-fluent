# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.functional import cached_property

from edw_fluent.models.page import SimplePage
from edw_fluent.models.related import EntityImage, EntityFile, PublicationComment
from edw_fluent.plugins.datamart.models import DataMartItem


class DataMartFluentMixin(object):

    def get_detail_page(self):
        """
        RUS: Для просмотра содержимого конкретной страницы
        """
        placeholders = DataMartItem.objects.filter(
            datamarts__in=[self.pk]
        ).values_list(
            'placeholder_id',
            flat=True
        )
        try:
            result = SimplePage.objects.filter(
                placeholder_set__id__in=placeholders
            ).exclude(
                translations__override_url='/'
            )[0]
        except IndexError:
            result = None
        return result


class ImagesFilesFluentMixin(object):

    @cached_property
    def ordered_images(self):
        """
        RUS: Возвращает список всех отсортированных изображений.
        """
        return list(self.get_ordered_images())

    def get_ordered_images(self):
        """
        RUS: Возвращает все отсортированные изображения.
        """
        return self.images.all().order_by('entityimage__order')

    @cached_property
    def gallery(self):
        """
        RUS: Получает список галерей.
        """
        return list(self.get_gallery())

    def get_gallery(self):
        """
        RUS: Создает галерею из изображений, связанных с данной публикацией и ее блокамии и отсортированных по порядку.
        """
        return EntityImage.objects.filter(entity=self, key=None).select_related('image').order_by('order')

    @cached_property
    def thumbnail(self):
        """
        RUS: Возвращает список миниатюр.
        """
        return list(self.get_thumbnail())

    def get_thumbnail(self):
        """
        RUS: Получает миниатюру по ключу, отсортированные по порядку.
        """
        return EntityImage.objects.filter(entity=self, key=EntityImage.THUMBNAIL_KEY).order_by('order')

    @cached_property
    def attachments(self):
        """
        RUS: Возвращает список вложений.
        """
        return list(self.get_attachments())

    def get_attachments(self):
        """
        RUS: Получает файлы по ключу, отсортированные по порядку.
        """
        return EntityFile.objects.filter(entity=self, key=None).order_by('order')

    @cached_property
    def thumbnails(self):
        """
        RUS: Получает миниатюры по ключу, отсортированные по порядку.
        Если миниатюра не выбрана, берется первая картинка по умолчанию, которая становится миниатюрой.
        Используется для рендера миниатюры в компоненте представления (summary-...-media.html)
        """
        thumbnails = [x.image for x in
                      EntityImage.objects.filter(entity=self, key=EntityImage.THUMBNAIL_KEY).order_by('order')]
        if thumbnails:
            return thumbnails
        else:
            thumbnails = [x.image for x in self.gallery]
            if len(thumbnails) == 0:
                thumbnails = self.ordered_images
            return thumbnails[:1]


class CommentsFluentMixin(object):

    @cached_property
    def ordered_comments(self):
        """
        RUS: Возвращает список всех отсортированных по ключу комментариев.
        """
        return list(self.get_ordered_comments())

    def get_ordered_comments(self):
        """
        RUS: Возвращает все отсортированные комментарии.
        """
        return PublicationComment.objects.filter(entity=self).order_by('key')

    @cached_property
    def default_comments(self):
        """
        RUS: Получает список комментариев не привязанных к блокам.
        """
        return list(self.get_default_comments())

    def get_default_comments(self):
        """
        RUS: Возвращает все не привязанных к блокам комментарии.
        """
        return self.get_ordered_comments().filter(key=None)
