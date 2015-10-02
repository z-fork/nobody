# -*- coding: utf-8 -*-

from nobody.libs.store import PickledRedis
from magnet.crawler import settings


r = PickledRedis(
    socket_timeout=0.5,  # seconds, see `socket.settimeout()`
    retry_on_timeout=True,
    **settings.REDIS_CONF
)
