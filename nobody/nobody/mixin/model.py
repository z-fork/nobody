# -*- coding: utf-8 -*-

from django.db import models


class DateTimeMixin(models.Model):

    class Meta(object):
        abstract = True

    create_time = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')


