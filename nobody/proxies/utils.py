# -*- coding: utf-8 -*-

from proxies.libs import pq, ps
from proxies.crawler.settings import ABANDON_PRIORITY


def clear_proxy_queue():
    pq.clear()


def clear_proxy_store():
    ps.clear()


def get_proxy():
    if pq.empty():
        proxies = ps.get_all_with_priority()

        for proxy, priority in proxies:
            if priority > ABANDON_PRIORITY:
                ps.delete(proxy)
            else:
                pq.put(proxy)

    return pq.get_nowait()


def get_priority(proxy):
    return ps.get_priority(proxy)


def add_or_update(proxy, priority):
    ps.add_or_update(priority, proxy)
