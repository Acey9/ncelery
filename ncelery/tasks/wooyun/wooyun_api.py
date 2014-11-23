#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    wooyun_api.py
#  Author  :    wanghui@
#  Project :    ncelery
#  Date    :    2013-06-03 03:03
#  Descrip :    wooyun api achieve.
#               The server logic code.
# -----------------------------------------------------

import time
import json

import taskconf
from ncelery.celery import get_task_logger
from ncelery.utils import _requests
from ncelery.exception import WooYunResultException

logger = get_task_logger('ncelery.third_notice')
API_SUBMIT = 'http://api.wooyun.org/bugs/submit/limit/%s'

class WooYun(_requests.Request):

    api_corp = taskconf.WOOYUN_API_CORP
    api_detail = taskconf.WOOYUN_API_DETAIL
    api_submit = API_SUBMIT

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __repr__(self):
        return "Wooyun api."

    def filterBug(self, alerted_bug, wooyun_result):
        new_bugs = {} 
        current_time = time.time()
        max_id, last_submit_time = alerted_bug
        for _id, bug in wooyun_result.iteritems():
            submit_time = 0
            try:
                _id = int(_id)
                submit_time = int(bug.get('timestamp'))
            except BaseException, e:
                logger.error('Wooyun data format error, id:%s, submit_time:%s [%s]', 
                        _id, submit_time, wooyun_result)
                raise WooYunResultException(e)

            if ((_id <= max_id and submit_time <= last_submit_time) or  
                    (current_time - submit_time) > taskconf.EXPIRED_INTERVAL):
                continue
            new_bugs.setdefault(_id, bug)
        return new_bugs

    def formatData(self, wooyun_res, api_type):
        bugs = {}
        for res in wooyun_res:
            res['api_type'] = api_type
            bugs.setdefault(res['id'], res)
        return bugs

    def getSubmit(self, limit=10):
        api = self.api_submit % limit
        data = self.urlOpen(api)
        value = self.parse(data)
        bugs = self.formatData(value, taskconf.WOOYUN_API_TYPE_SUBMIT)
        return bugs

    def getBugsByCorp(self, limit=500):
        url = "%s/%s" % (self.api_corp, limit) 
        data = self.urlOpen(url)
        value = self.parse(data)
        bugs = self.formatData(value, taskconf.WOOYUN_API_TYPE_CROP)
        return bugs

    def getBugs(self, limit=500, alerted_bug=(0, 0)):
        submit_bug = {}
        try:
            submit_bug = self.getSubmit(limit)
        except WooYunResultException, e:
            logger.error('get submit bug. WooYunResultException %s', e)
        except BaseException, e:
            logger.error('get submit bug. %s', e)

        corp_bugs = self.getBugsByCorp(limit)
        corp_bugs.update(submit_bug)
        all_bugs = corp_bugs
        new_bugs = self.filterBug(alerted_bug, all_bugs)
        return new_bugs

    def getBugDetail(self, bugid):
        url = "%s/%s" % (self.api_detail, str(bugid))
        data = self.urlOpen(url)
        value = self.parse(data)
        if type(value) != dict:
            raise WooYunResultException('Invalid data format.')
        return value

    def parse(self, data):
        try:
            data = json.loads(data)
            return data
        except BaseException, e:
            logger.error('Parse wooyun data error.[%s], data:[%s]', e, data)
            raise WooYunResultException(e)

    def urlOpen(self, url):
        try:
            res = self.get(url)
            value = res.text
        except BaseException, e:
            logger.error('Connect to %s failed. [%s]', url, e)
            raise WooYunResultException(e)
        return value

