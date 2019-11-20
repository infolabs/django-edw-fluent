# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from future.utils import python_2_unicode_compatible

from chakert import Typograph

from fluent_contents.extensions import PluginHtmlField
from fluent_contents.models import ContentItem
from fluent_contents.utils.filters import apply_filters

from edw_fluent.utils import remove_unprintable


@python_2_unicode_compatible
class BlockItem(ContentItem):

    SHORT_SUBTITLE_MAX_WORDS_COUNT = 12
    SHORT_SUBTITLE_MAX_CHARS_COUNT = 120
    SHORT_SUBTITLE_TRUNCATE = '...'

    text = PluginHtmlField(_('text'), blank=True)
    text_final = models.TextField(editable=False, blank=True, null=True)
    subjects = models.ManyToManyField('Publication', related_name='block_subjects',
                                      db_table='{}_block_subjects'.format(settings.EDW_APP_LABEL))

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Block')
        verbose_name_plural = _('Blocks')

    def __str__(self):
        return Truncator(
            Truncator(strip_tags(self.text)).words(
                self.SHORT_SUBTITLE_MAX_WORDS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE)
        ).chars(self.SHORT_SUBTITLE_MAX_CHARS_COUNT, truncate=self.SHORT_SUBTITLE_TRUNCATE)

    def full_clean(self, *args, **kwargs):
        # This is called by the form when all values are assigned.
        # The pre filters are applied here, so any errors also appear as ValidationError.
        super(BlockItem, self).full_clean(*args, **kwargs)

        # todo: переделать через фильтры и сделать фильтр типографа последним, remove_unprintable сделать тоже фильтром
        self.text = Typograph.typograph_html(remove_unprintable(self.text), 'ru')

        self.text, self.text_final = apply_filters(self, self.text, field_name='text')

        if self.text_final == self.text:
            # No need to store duplicate content:
            self.text_final = None
