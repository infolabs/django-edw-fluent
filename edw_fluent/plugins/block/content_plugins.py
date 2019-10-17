# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fluent_contents.extensions import plugin_pool

from edw_fluent.plugins.block.pluginbase import BaseBlockPlugin


@plugin_pool.register
class BlockPlugin(BaseBlockPlugin):
    pass