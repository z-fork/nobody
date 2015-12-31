# -*- coding: utf-8 -*-

from magnet.crawler.contrib.store import r as r_store

from proxies.crawler.settings import PROXY_STORE_KEY, PROXY_QUEUE_KEY


class ProxyQueue(object):
    def __init__(self, r):
        self.__db = r
        self.key = PROXY_QUEUE_KEY

    def size(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.size() == 0

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        return item

    def get_nowait(self):
        return self.get(False)

    def clear(self):
        self.__db.delete(self.key)


class ProxyStore(object):
    def __init__(self, r):
        self.__db = r
        self.key = PROXY_STORE_KEY

    def size(self):
        return self.__db.zcard(self.key)

    def empty(self):
        return self.size() == 0

    def add_or_update(self, proxy, priority):
        self.__db.zadd(self.key, proxy, priority)

    def get_all_with_priority(self):
        return self.__db.zrange(self.key, 0, -1, withscores=True)

    def get_priority(self, proxy):
        return self.__db.zscore(self.key, proxy)

    def delete(self, proxy):
        self.__db.zrem(self.key, proxy)

    def clear(self):
        self.__db.delete(self.key)


pq = ProxyQueue(r_store)
ps = ProxyStore(r_store)
