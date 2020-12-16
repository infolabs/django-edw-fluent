# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from edw.rest.serializers.filer_fields import FilerImageField
from edw_fluent.models.related import PublicationComment


class PublicationCommentSerializer(serializers.ModelSerializer):

    bind_to = serializers.ListField(
        child=serializers.CharField(),
        source="_bind_to"
    )

    logo = FilerImageField(max_length=None, use_url=True, upload_folder_name=_('Comments logos'))

    class Meta:
        model = PublicationComment
        fields = ['origin_name', 'text', 'origin_url', 'logo', 'bind_to', 'key']
        list_serializer_class = serializers.ListSerializer

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'detail')
        super(PublicationCommentSerializer, self).__init__(*args, **kwargs)
