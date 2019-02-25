# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

FILE_UPLOAD_TO = getattr(settings, 'FILE_UPLOAD_TO', '.')
