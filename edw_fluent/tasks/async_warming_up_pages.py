import json
from io import StringIO

from celery import shared_task

from django.core.management import call_command

from edw_fluent.contrib.exceptions import WarmingUpException

@shared_task(name='async_warming_up_pages')
def async_warming_up_pages(**kwargs):
    """
    ENG: For optimal task performance, the periodic task should be every minute.

    RUS: Для оптимальной работы задачи, периодическая задача должна выполняться каждую минуту.
    """
    only_main_page = kwargs.get('only_main_page', False)
    out = StringIO()
    call_command('warming_up_pages', stdout=out, main_page=only_main_page)
    result = json.loads(out.getvalue())

    if result.get('errors'):
        raise WarmingUpException(urn=result.get('urn', None), error=result.get('errors'))
    return result