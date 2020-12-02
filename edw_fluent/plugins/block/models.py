# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from future.utils import python_2_unicode_compatible

from chakert import Typograph
from fluent_contents.extensions import PluginHtmlField
from fluent_contents.models import ContentItem
from fluent_contents.utils.filters import apply_filters

from django.utils import six
from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from edw_fluent.utils import remove_unprintable


@python_2_unicode_compatible
class BlockItem(ContentItem):
    """
    RUS: Класс экземпляра блока (BlockItem).
    Определяет поля и их значения.
    """
    SHORT_SUBTITLE_MAX_WORDS_COUNT = 12
    SHORT_SUBTITLE_MAX_CHARS_COUNT = 120
    SHORT_SUBTITLE_TRUNCATE = '...'

    text = PluginHtmlField(_('text'), blank=True)
    text_final = models.TextField(editable=False, blank=True, null=True)
    subjects = models.ManyToManyField('Publication', related_name='block_subjects',
                                      db_table='{}_block_subjects'.format(settings.EDW_APP_LABEL))

    class Meta:
        """
        RUS: Метаданные класса BlockItem.
        """
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Block')
        verbose_name_plural = _('Blocks')

    def __str__(self):
        """
        RUS: При превышении длины подзаголовок обрезается до нужного количества символов.
        Строковое представление данных.
        """
        return Truncator(
            Truncator(strip_tags(self.text)).words(
                self.SHORT_SUBTITLE_MAX_WORDS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE)
        ).chars(self.SHORT_SUBTITLE_MAX_CHARS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE)

    def full_clean(self, *args, **kwargs):
        """
        RUS: Проверка данных текста формы.
        Текст должен быть проверен типографом и удалить непечатные символы.
        """
        # This is called by the form when all values are assigned.
        # The pre filters are applied here, so any errors also appear as ValidationError.
        super(BlockItem, self).full_clean(*args, **kwargs)

        # todo: переделать через фильтры и сделать фильтр типографа последним, remove_unprintable сделать тоже фильтром
        self.text = Typograph.typograph_html(remove_unprintable(self.text), 'ru')

        self.text, self.text_final = apply_filters(self, self.text, field_name='text')

        if self.text_final == self.text:
            # No need to store duplicate content:
            self.text_final = None

    def get_stripped_text(self, with_dots_in_headings=False):
        text = self.text

        def format_str(text_to_format, expr, join_with_str):
            if six.PY2:
                expr = expr.decode('raw_unicode_escape')
            pattern = re.compile(expr, re.UNICODE)

            formatted_text = re.sub(
                pattern,
                r'\g<1>{}\g<2>'.format(join_with_str),
                text_to_format,
            )

            return formatted_text

        block_tags_regexp = r'([\w«»\'"])(<\/(?:h[1-6]|p|div|ul|ol|link)\b[^>]*>)'
        other_tags_regexp = r'([\w«»\'"])(<\/(?!=:h[1-6]|p|div|ul|ol)[^>]*>)'

        text = format_str(text, block_tags_regexp, '. ')
        text = format_str(text, other_tags_regexp, ' ')

        # deleting excessive spaces
        stripped_text = strip_tags(text)

        finalized_text = re.sub(
            r'\s{2,}',
            ' ',
            stripped_text,
        )

        return finalized_text.strip()
