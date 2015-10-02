# -*- coding: utf-8 -*-

from redis import StrictRedis
import pickle

from django.conf import settings


class PickledRedis(StrictRedis):

    def pickle_get(self, name):
        pickled_value = super(PickledRedis, self).get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def pickle_set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(PickledRedis, self).set(
            name, pickle.dumps(value),
            ex, px, nx, xx
        )


r = PickledRedis(
    socket_timeout=0.5,  # seconds, see `socket.settimeout()`
    retry_on_timeout=True,
    **settings.REDIS_CONF
)
