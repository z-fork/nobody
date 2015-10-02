# -*- coding: utf-8 -*-


class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, r, name, namespace='queue'):
        self.__db = r
        self.key = '%s:%s' % (namespace, name)
    
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
