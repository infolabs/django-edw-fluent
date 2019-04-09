# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from fluent_contents.admin import PlaceholderFieldAdmin
from fluent_contents.models import Placeholder

from edw.admin.entity import (
    EntityCharacteristicOrMarkInline,
    EntityRelatedDataMartInline,
)
from edw.admin.entity.forms import EntityAdminForm
from edw.admin.entity.entity_image import EntityImageInline
from edw.admin.entity.entity_file import EntityFileInline
from edw.admin.entity import EntityChildModelAdmin

from edw_fluent.plugins.block.models import BlockItem

from edw_fluent.admin.forms.image import PublicationImageInlineForm
from edw_fluent.admin.forms.file import PublicationFileInlineForm


#===========================================================================================
# PublicationImageInline
#===========================================================================================
class PublicationImageInline(EntityImageInline):

    form = PublicationImageInlineForm

    def get_formset(self, request, obj=None, **kwargs):
        self.form.publication = obj
        return super(PublicationImageInline, self).get_formset(request, obj, **kwargs)


#===========================================================================================
# PublicationFileInline
#===========================================================================================
class PublicationFileInline(EntityFileInline):

    form = PublicationFileInlineForm

    def get_formset(self, request, obj=None, **kwargs):
        self.form.publication = obj
        return super(PublicationFileInline, self).get_formset(request, obj, **kwargs)


#===========================================================================================
# PublicationAdmin
#===========================================================================================
class BasePublicationAdmin(PlaceholderFieldAdmin, EntityChildModelAdmin):

    base_form = EntityAdminForm

    save_on_top = True

    base_fieldsets = (
        (None, {
            'fields':
                ('title', 'subtitle', 'lead', 'pinned', 'terms', 'statistic', 'created_at', 'unpublish_at', 'active'),
        }),
        (_('Content blocks'), {
            'fields':
                ('content',),
        }),
    )

    class Media:
        css = {
            'all': [
                '/static/css/admin/entity.css',
            ]
        }

    search_fields = ('title', 'subtitle', 'lead')

    list_display = ['title', 'id', 'created_at', 'pinned', 'active', 'statistic']

    inlines = [
        EntityCharacteristicOrMarkInline,
        EntityRelatedDataMartInline,
        PublicationImageInline,
        PublicationFileInline,
    ]

    def view_on_site(self, obj):
        return obj.get_detail_url()

    publication_id_for_formfield = None

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.publication_id_for_formfield = obj.id
        return super(BasePublicationAdmin, self).get_form(request, obj, **kwargs)

    def save_related(self, request, form, formsets, change):
        super(BasePublicationAdmin, self).save_related(request, form, formsets, change)

        entity_id = int(form.instance.id)

        placeholders = Placeholder.objects.filter(
            parent_id=entity_id,
        )

        if placeholders:

            placeholder = placeholders[0]

            blockitems = BlockItem.objects.filter(
                placeholder_id=placeholder.id,
            )

            if len(blockitems) == 0:
                BlockItem.objects.create(
                    placeholder_id=placeholder.id,
                    parent_id=entity_id,
                    parent_type_id=placeholder.parent_type_id,
                )
