# -*- coding: utf-8 -*-

from logging import getLogger, INFO


_logger = getLogger('nobody')


def send_log(channel, message, data=None, log_level=INFO):
    _logger.log(log_level, message, extra=data)
