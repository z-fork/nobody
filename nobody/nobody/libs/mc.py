# -*- coding: utf-8 -*-

import inspect
from functools import wraps
import time

from django.core.cache import cache as mc

import re


class Empty(object):

    def __call__(self, *a, **kw):
        return empty

    def __nonzero__(self):
        return False

    def __contains__(self, item):
        return False

    def __repr__(self):
        return '<Empty Object>'

    def __str__(self):
        return ''

    def __eq__(self, v):
        return isinstance(v, Empty)

    def __getattr__(self, name):
        if not name.startswith('__'):
            return empty
        raise AttributeError(name)

    def __len__(self):
        return 0

    def __getitem__(self, key):
        return empty

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

empty = Empty()


str_pattern = re.compile(r'%\w')
obj_pattern = re.compile(r'\{(\w+(\.\w+|\[\w+\])*)\}')


__formatter = {}


def formatter(text):
    """
    format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    class Obj: id = 3
    format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    """
    def gen_attr_value(name, attr_list, *a, **kw):
        if name.isdigit():
            target = a[int(name)]
        else:
            target = kw[name]

        for attr in attr_list:
            target = getattr(target, attr)

        return target

    def translator(_text):
        if '.' in _text:
            attrs = _text.split('.')
            name = attrs.pop(0)
            return lambda *a, **kw: gen_attr_value(name, attrs, *a, **kw)
        else:
            if _text.isdigit():
                return lambda *a, **kw: a[int(_text)]
            return lambda *a, **kw: kw[_text]

    args = [translator(obj) for obj, attr in obj_pattern.findall(text)]

    if args:
        if str_pattern.findall(text):
            raise Exception()

        # TODO ...pattern.sub
        f = obj_pattern.sub('%s', text)

        return lambda *a, **kw: f % tuple([k(*a, **kw) for k in args])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        n = len(str_pattern.findall(text))
        return lambda *a, **kw: text % tuple(a[:n])


def _format(text, *a, **kw):
    f = __formatter.get(text)
    if f is None:
        f = formatter(text)
        __formatter[text] = f
    return f(*a, **kw)


def gen_key_factory(key_pattern, args, defaults):
    args_dic = dict(zip(args[-len(defaults):], defaults)) if defaults else {}

    # if callable(key_pattern):
    #     names = inspect.getargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args_dic.copy()
        aa.update(zip(args, a))
        aa.update(kw)
        # if callable(key_pattern):
        #     key =
        # else:
        key = _format(key_pattern, *[aa[n] for n in args], **aa)
        return key and key.replace(' ', '_'), aa
    return gen_key


def cache(key_pattern, mc=mc, expire=0, max_retry=0):
    def _(func):
        args, var, kw, defaults = inspect.getargspec(func)
        gen_key = gen_key_factory(key_pattern, args, defaults)

        @wraps(func)
        def __(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return func(*a, **kw)
            force = kw.pop('force', False)
            r = mc.get(key) if not force else None

            # anti miss-storm
            retry = max_retry
            while r is None and retry > 0:
                # when node is down, add() will failed
                if mc.add(key + '#mutex', 1, int(max_retry * 0.1)):
                    break
                time.sleep(0.1)
                r = mc.get(key)
                retry -= 1

            if r is None:
                r = func(*a, **kw)
                if r is not None:
                    # TODO model object 不用pikle?
                    mc.set(key, r, expire)
                if max_retry > 0:
                    mc.delete(key + '#mutex')

            if isinstance(r, Empty):
                r = None

            return r

        __.original_function = func
        return __
    return _


