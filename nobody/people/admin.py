# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
    DoubanPeople,
    DoubanGroup
)

admin.site.register(DoubanPeople)
admin.site.register(DoubanGroup)

