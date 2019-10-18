#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext as _

from edw_fluent.plugins.hottag.tasks.update_hot_tags import update_hot_tags


class Command(NoArgsCommand):
    help = _(
        "Update HotTag "
    )

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--delta_days',
            dest='delta_days',
            type=int,
            default=0,
            help=_('Count of days left for update')
        ),
    )
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--full_update',
            dest='full_update',
            type='choice',
            choices = ("false", "true"),
            default='false',
            help=_('Update not empty publications for best match')
        ),
    )

    def handle_noargs(self, **options):
        delta_days = options.get('delta_days')
        full_update = options.get('full_update')
        res = update_hot_tags(delta_days, full_update)
        print 'Total tags found - {} \n' \
              'Total updated tags - {} \n' \
              'Total deleted tags - {} \n' \
              'Found target publication for - {} tags,\n' \
              'Not found target publication for - {} tags,\n'\
              'Tags with errors - {} tags'.format(
            res['total_tag_count'],
            res['updeted_tag_count'],
            res['deleted_tag_count'],
            res['founded_target_count'],
            res['empty_target_count'],
            res['update_errors_count'],
        )