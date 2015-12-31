# -*- coding: utf-8 -*-

from proxies.utils import add_or_update


class RedisPipeline(object):
    def process_item(self, item, spider):
        add_or_update(item['proxy'], item['priority'])
        return item
