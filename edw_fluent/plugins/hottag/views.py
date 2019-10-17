# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import simplejson as json

from django.http import HttpResponse

from edw_fluent.plugins.hottag.utils import turncat, search_tag


def hottagsearch(request):

    search_text = request.GET.get('q', '')
    result = search_tag(search_text)

    if result and result.object:
        # TODO: result may be not Entity instance
        suggestion = {
                'title': turncat(result.object.entity_name),
                'model': result.object.entity_model,
                'model_id': result.object.id,
                'url': result.object.get_detail_url()
            }
    else:
        suggestion = {}

    the_data = json.dumps(suggestion)
    return HttpResponse(the_data, content_type='application/json')