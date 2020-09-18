# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from edw_fluent.models.related import EntityImage
from edw_fluent.plugins.block.models import BlockItem


class PublicationImageInlineForm(forms.ModelForm):
    """
    Определяет форму и поля загрузчика изображений в публикациях
    """
    AVAILABLE_CHOICES = (
        (None, _("Default")),
        (EntityImage.THUMBNAIL_KEY, _("Thumbnail"))
    )

    key = forms.ChoiceField(label=_("Info block"), required=False, choices=AVAILABLE_CHOICES)

    image_author = forms.CharField(label=_("Author"), required=False, max_length=255)

    image_caption = forms.CharField(label=_("Title"), required=False, max_length=255)

    def __init__(self, *args, **kwargs):
        """
        Конструктор класса
        """
        super(PublicationImageInlineForm, self).__init__(*args, **kwargs)
        entity = getattr(self, 'entity', None)
        available_choices = list(self.AVAILABLE_CHOICES)
        try:
            for block in entity.content.contentitems.filter(instance_of=BlockItem):
                available_choices.append((int(block.pk), str(block.__str__())))
        except ObjectDoesNotExist:
            pass
        self.fields['key'].choices = available_choices

    def clean(self):
        """
        Словарь проверенных и нормализованных данных формы загрузки изображений в публикациях
        """
        cleaned_data = super(PublicationImageInlineForm, self).clean()
        key = cleaned_data['key']
        if key == '':
            cleaned_data['key'] = None
        return cleaned_data
