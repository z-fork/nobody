# -*- coding: utf-8 -*-
"""
TODO...

reactor cann't run again. so....
"""

# from scrapy.conf import settings
# from scrapy.command import ScrapyCommand
# from scrapy.crawler import Crawler
#
# from magnet.crawler import settings as crawler_settings
# from magnet.crawler.spiders.douban import PeopleCrawler
#
#
# class Command(ScrapyCommand):
#
#     requires_project = False
#
#     def run(self, args=None, opts=None):
#         self._run_crawler(PeopleCrawler())
#
#     @staticmethod
#     def _run_crawler(crawler):
#         settings.overrides.update(crawler_settings.__dict__)
#         _crawler = Crawler(settings)
#
#         import scrapy.project
#         if hasattr(scrapy.project, 'crawler'):
#             _crawler.uninstall()
#         _crawler.install()
#
#         _crawler.configure()
#         _crawler.crawl(crawler)
#
#         _crawler.start()
#
#
# if __name__ == "__main__":
#     cmd = Command()
#     cmd.run()
