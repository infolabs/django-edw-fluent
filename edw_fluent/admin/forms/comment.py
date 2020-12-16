# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from edw_fluent.plugins.block.models import BlockItem


class PublicationCommentInlineForm(forms.ModelForm):
    """
    Определяет форму и поля
    """
    AVAILABLE_CHOICES = (
        (None, _("Default")),
    )

    key = forms.ChoiceField(label=_("Info block"), required=False, choices=AVAILABLE_CHOICES)

    def __init__(self, *args, **kwargs):
        """
        Конструктор класса
        """
        super(PublicationCommentInlineForm, self).__init__(*args, **kwargs)
        entity = getattr(self, 'entity', None)
        available_choices = list(self.AVAILABLE_CHOICES)
        if entity and hasattr(entity, 'content'):
            try:
                for block in entity.content.contentitems.filter(instance_of=BlockItem):
                    available_choices.append((int(block.pk), str(block.__str__())))
            except ObjectDoesNotExist:
                pass
        self.fields['key'].choices = available_choices

    def clean(self):
        """
        Словарь проверенных и нормализованных данных формы
        """
        cleaned_data = super(PublicationCommentInlineForm, self).clean()
        key = cleaned_data['key']
        if key == '':
            cleaned_data['key'] = None
        return cleaned_data
