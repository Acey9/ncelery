#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    tasks.py
#  Author  :    wanghui@
#  Project :    ncelery
#  Date    :    2013-06-03 03:15
#  Descrip :    Third-party security notices task module.
#               Only for writing celery task code.
# -----------------------------------------------------

#Import ncelery project celery instance
from ncelery.celery import ncelery 

#Import the module of logging
from ncelery.celery import get_task_logger

#Service logic
import wooyun_api

logger = get_task_logger('ncelery.wooyun')

#Create a task by using the task() decorator
@ncelery.task(ignore_result=False)
def getBugs(limit=500, alerted_bug=(0, 0)):
    """Get corpname notice from wooyun.com.

    :param limit: The bug number. Default is 10.
    :type limit: int.
    :param alerted_bug: The last alerted bug id and submit time. Default is (0, 0)
    :type alerted_bug: tuple.
    :returns: {id1:None, id2:None}
    :raises: WooYunResultException

    """
    logger.info('get bugs.')
    with wooyun_api.WooYun() as wy:
        data = wy.getBugs(limit, alerted_bug)
        return data #return task result

@ncelery.task(ignore_result=False)
def getBugDetail(bug_id):
    """Get corpname notice from wooyun.com.

    :param bug_id: The bug id
    :type bug_id: int.
    :returns: {u'status':u'1', u'comment':u'26', u'description':u'xxxx', ...}
    :raises: WooYunResultException

    """
    logger.info('get bug detail infomation.')
    #task_id = getBugDetail.request.id
    #task_name = getBugDetail.name
    with wooyun_api.WooYun() as wy:
        data = wy.getBugDetail(bug_id)
        return data #return task result
