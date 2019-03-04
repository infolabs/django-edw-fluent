# -*- coding: utf-8 -*-
from django.db.utils import ProgrammingError

try:
    from edw_fluent.signals.handlers import (
        page_layout,
        template,
        entity,
        data_mart,
        term,
        simple_page
    )
except (AttributeError, ProgrammingError) as e:
    # initial migrations hack
    print("*** INITIAL MIGRATIONS HACK ***")
    print e.args