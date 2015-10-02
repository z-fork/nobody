# -*- coding: utf-8 -*-


class DjangoModelPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item
