# -*- coding: utf-8 -*-

from django.core.management import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()

        sql = 'select page from douban_people group by page having count(page) > 1'
        cursor.execute(sql)

        pages = [page for (page, ) in cursor.fetchall()]

        if not pages:
            raise CommandError('...Why filter?')

        for page in pages:
            sql = 'select id from douban_people where page="%s" order by id' % page
            cursor.execute(sql)

            ids = [_id for (_id, ) in cursor.fetchall()]

            print ids

            sql = 'delete from douban_people where id in (%s)' % ','.join(map(str, ids[1:]))

            cursor.execute(sql)
