# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.djangoitem import DjangoItem

from people.models import (
    DoubanPeople,
    DoubanGroup,
    DoubanJoins,
)


class PeopleItem(DjangoItem):
    django_model = DoubanPeople
    image_urls = scrapy.Field()


class GroupItem(DjangoItem):
    django_model = DoubanGroup


class JoinsItem(DjangoItem):
    django_model = DoubanJoins
