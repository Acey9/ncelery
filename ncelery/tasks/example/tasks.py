from __future__ import absolute_import

from celery import group, chord
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded

from ncelery.celery import ncelery 
from ncelery.celery import get_task_logger

logger = get_task_logger('ncelery.example')

#@ncelery.task(ignore_result=False, throws=(SoftTimeLimitExceeded, TimeLimitExceeded))
@ncelery.task(ignore_result=False)
def add(x, y):
    logger.info("add...")
    #import time
    #time.sleep(10)
    return x+y 

@ncelery.task(ignore_result=False)
def _link(x, y):
    logger.info("_link")
    print x, y
    return x, y

@ncelery.task(ignore_result=False)
def _chord():
    logger.info("_chord...")
    job = group(add.s(1, 2),
            add.s(3, 4)
            )
    chord(job)(_link.s(1))
    return
