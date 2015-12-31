# -*- coding: utf-8 -*-

from annoying.functions import get_object_or_None
from django.db import models

from nobody.libs.mc import cache
from nobody.mixin.model import DateTimeMixin

_MC_KEY_PEOPLE = "/people/%s/:model"


class DoubanPeople(models.Model):
    class Meta:
        db_table = 'douban_people'
        verbose_name_plural = verbose_name = 'douban-people'

    page = models.CharField(verbose_name='page', unique=True, max_length=255)
    name = models.CharField(verbose_name='name', max_length=64)
    location = models.CharField(verbose_name='location', max_length=25)
    refer = models.CharField(verbose_name='refer', max_length=255, default='')
    html = models.TextField(verbose_name='html', default='')

    @classmethod
    def get_by_url(cls, page):
        return get_object_or_None(cls, page=page)

    @classmethod
    def exist_duplication(cls, page):
        return cls.get_by_url(page)

    @classmethod
    @cache(_MC_KEY_PEOPLE % "{pk}")
    def get(cls, pk):
        return get_object_or_None(cls, pk=pk)

    @classmethod
    def get_all_ids(cls):
        return cls.objects.all().values_list('id', flat=True)

    @classmethod
    def get_all(cls):
        return [cls.get(pk) for pk in cls.get_all_ids()]

    @classmethod
    def get_multi(cls, ids):
        objects = [cls.get(pk) for pk in ids]
        return filter(None, objects)

    @classmethod
    def filter(cls, *args, **kwargs):
        ids = cls.objects.filter(*args, **kwargs) \
                         .order_by('id') \
                         .values_list('id', flat=True)
        return cls.get_multi(ids)


class DoubanGroup(models.Model):
    class Meta:
        db_table = 'douban_group'
        verbose_name_plural = verbose_name = 'douban-group'

    page = models.CharField(verbose_name='page', unique=True, max_length=255)
    name = models.CharField(verbose_name='name', max_length=64)
    num = models.IntegerField(verbose_name='num')


class DoubanJoins(models.Model):
    class Meta:
        db_table = 'douban_joins'
        verbose_name_plural = verbose_name = 'douban-joins'
        unique_together = (('people', 'group'), )

    people = models.CharField(verbose_name='people', max_length=255)
    group = models.CharField(verbose_name='group', max_length=255)


class DoubanTopic(DateTimeMixin):
    class Meta:
        db_table = 'douban_topic'
        verbose_name_plural = verbose_name = 'douban-topic'

    page = models.CharField(verbose_name='page', unique=True, max_length=255)
    group = models.CharField(verbose_name='group', max_length=255)
    num = models.IntegerField(verbose_name='num')
    content = models.TextField(verbose_name='content')
    origin_time = models.DateTimeField(verbose_name='origin_time')


class DoubanTopicPeople(DateTimeMixin):
    class Meta:
        db_table = 'douban_topic_people'
        verbose_name_plural = verbose_name = 'douban-topic-people'
        unique_together = (('people', 'to'), )

    topic = models.CharField(verbose_name='topic', max_length=255)
    origin = models.CharField(verbose_name='origin', max_length=255)
    people = models.CharField(verbose_name='people', max_length=255)
    to = models.CharField(verbose_name='to', max_length=255)
    num = models.IntegerField(verbose_name='num')
