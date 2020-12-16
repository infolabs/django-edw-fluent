# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from edw_fluent.models.related import PublicationComment


class PublicationCommentSerializer(serializers.ModelSerializer):

    bind_to = serializers.ListField(
        child=serializers.CharField(),
        source="_bind_to"
    )

    class Meta:
        model = PublicationComment
        fields = ['origin_name', 'text', 'origin_url', 'logo', 'bind_to', 'key']
        list_serializer_class = serializers.ListSerializer

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'detail')
        super(PublicationCommentSerializer, self).__init__(*args, **kwargs)
