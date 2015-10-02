# -*- coding: utf-8 -*-

from annoying.functions import get_object_or_None
from django.db import models


class NobodyProxy(models.Model):
    class Meta:
        db_table = 'douban_proxy'
        verbose_name_plural = verbose_name = 'douban-proxy'

    proxy = models.CharField(verbose_name='proxy', max_length=30)
    priority = models.IntegerField(verbose_name='priority')

    def __str__(self):
        return self.proxy

    @classmethod
    def get(cls, pk):
        return get_object_or_None(cls, pk=pk)

    @classmethod
    def get_all_ids(cls):
        return cls.objects.all().order_by('-priority').values_list('id', flat=True)

    @classmethod
    def get_all(cls):
        proxies = [cls.get(pk) for pk in cls.get_all_ids()]
        return filter(None, proxies)

    @classmethod
    def get_by_proxy(cls, proxy):
        return get_object_or_None(cls, proxy=proxy)

    @classmethod
    def create(cls, proxy, priority):
        return cls.objects.create(
            proxy=proxy,
            priority=priority,
        )

    @classmethod
    def get_multi(cls, ids):
        objects = [cls.get(pk) for pk in ids]
        return filter(None, objects)

    @classmethod
    def filter(cls, *args, **kwargs):
        ids = cls.objects.filter(*args, **kwargs) \
                         .order_by('-priority') \
                         .values_list('id', flat=True)
        return cls.get_multi(ids)
