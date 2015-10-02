# -*- coding: utf-8 -*-

from django.core.management import BaseCommand, CommandError
from django.db import connection

from magnet.crawler.contrib.store import r


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()

        sql = 'select page from douban_people order by id limit 100000'
        cursor.execute(sql)

        pages = [page for (page, ) in cursor.fetchall()]

        if not pages:
            raise CommandError('...Why ?')

        joins_pages = lambda x: x + 'joins/'
        for page in map(joins_pages, pages):
            r.lpush('spider:start_urls', page)
