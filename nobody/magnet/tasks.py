# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger

from nobody.libs.mq import mq
# from nobody.libs.store import r

logger = get_task_logger(__name__)


@mq.task
def test_task():
    logger.info(".....%s" % __name__)
