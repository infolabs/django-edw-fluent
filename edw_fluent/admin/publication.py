# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from fluent_contents.admin import PlaceholderFieldAdmin
from fluent_contents.plugins.rawhtml.models import RawHtmlItem

from edw.admin.entity import (
    EntityRelationInline,
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
from edw_fluent.utils import remove_emoji


#===========================================================================================
# PublicationImageInline
#===========================================================================================
class PublicationImageInline(EntityImageInline):
    """
    Определяет форму загрузчика изображений в публикациях
    """
    form = PublicationImageInlineForm

    def get_formset(self, request, obj=None, **kwargs):
        """
        Возвращает набор форм загрузчика изображений в публикациях
        """
        self.form.entity = obj
        return super(PublicationImageInline, self).get_formset(request, obj, **kwargs)


#===========================================================================================
# PublicationFileInline
#===========================================================================================
class PublicationFileInline(EntityFileInline):
    """
    Определяет форму загрузчика файлов в публикациях
    """
    form = PublicationFileInlineForm

    def get_formset(self, request, obj=None, **kwargs):
        """
        Возвращает набор форм загрузчика файлов в публикациях
        """
        self.form.entity = obj
        return super(PublicationFileInline, self).get_formset(request, obj, **kwargs)


#===========================================================================================
# PublicationAdmin
#===========================================================================================
class BasePublicationAdmin(PlaceholderFieldAdmin, EntityChildModelAdmin):
    """
    Базовая административная форма создания/редактирования публикаций
    """
    base_form = EntityAdminForm

    save_on_top = True

    base_fieldsets = (
        (None, {
            'fields':
                ('title', 'subtitle', 'lead', 'tags', 'pinned', 'terms',
                 'statistic', 'created_at', 'unpublish_at', 'active'),
        }),
        (_('Content blocks'), {
            'fields':
                ('content',),
        }),
    )

    class Media:
        """
        Подключаемые стили CSS
        """
        css = {
            'all': [
                '/static/css/admin/entity.css',
            ]
        }

    search_fields = ('title', 'id', 'subtitle', 'lead')

    list_display = ['title', 'id', 'created_at', 'pinned', 'active', 'statistic']

    inlines = [
        EntityCharacteristicOrMarkInline,
        EntityRelationInline,
        EntityRelatedDataMartInline,
        PublicationImageInline,
        PublicationFileInline,
    ]

    def view_on_site(self, obj):
        """
        Формирует url публикации при просмотре на сайте
        """
        return obj.get_detail_url()

    publication_id_for_formfield = None

    def get_form(self, request, obj=None, **kwargs):
        """
        Добавляет в форму модель администратора
        """
        if obj:
            self.publication_id_for_formfield = obj.id
        return super(BasePublicationAdmin, self).get_form(request, obj, **kwargs)

    def save_related(self, request, form, formsets, change):
        """
        Сохраняет связанные модели объектов, определяет placeholder и создает текстовый блок
        """

        # remove emoji from html items
        for fs in formsets:
            for f in fs:
                if not f.is_valid():
                    continue
                obj = f.save(commit=False)
                if isinstance(obj, RawHtmlItem):
                    obj.html = remove_emoji(obj.html)

        super(BasePublicationAdmin, self).save_related(request, form, formsets, change)

        entity_id = int(form.instance.id)

        placeholder = form.instance.get_or_create_placeholder()
        blockitems = BlockItem.objects.filter(
            placeholder_id=placeholder.id,
        )

        if len(blockitems) == 0:
            BlockItem.objects.create(
                placeholder_id=placeholder.id,
                parent_id=entity_id,
                parent_type_id=placeholder.parent_type_id,
            )
