# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from future.utils import python_2_unicode_compatible

from fluent_contents.models import ContentItem

from page_builder.fields import BuilderTemplateField


from edw_fluent.models.page_builder import get_page_builder_elements_by_model


@python_2_unicode_compatible
class TemplateItem(ContentItem):
    template = BuilderTemplateField(
        verbose_name=_('Template'),
        max_length=255,
        null=True,
        blank=True,
        elements=get_page_builder_elements_by_model('templateitem'),
    )

    class Meta:
        app_label = settings.EDW_APP_LABEL
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return "{}: {}".format(self._meta.verbose_name, self.template)
