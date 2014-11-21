#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    taskconf.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-11-21 17:26
#  Descrip :    
# -----------------------------------------------------

from datetime import timedelta

###################include app########################

INCLUDE_APP = ['ncelery.tasks.wooyun.tasks',]

###################tasks routes#######################
#Note: One module one queue
CELERY_ROUTES = {
        "ncelery.tasks.wooyun.tasks.getBugs":{
            "queue":"ncq.wooyun"
            },
        "ncelery.tasks.wooyun.tasks.getBugDetail":{
            "queue":"ncq.wooyun"
            },
        }

CELERYBEAT_SCHEDULE = {
        }

######################celery annotations###############
#This setting can be used to rewrite any task attribute from the configuration.
#CELERY_ANNOTATIONS = {"*":{"time_limit":5, "soft_time_limit":3}}
CELERY_ANNOTATIONS = {
        }

#API key
WOOYUN_API_KEY = "yohouhou"
#Get has authorized the bugs
WOOYUN_API_CORP = 'http://api.wooyun.org/sec/auth/%s/bugs/type/2/limit/' % WOOYUN_API_KEY
#Get bug detail infomation
WOOYUN_API_DETAIL = 'http://api.wooyun.org/sec/auth/%s/bug' % WOOYUN_API_KEY
#expired 7 days not alert.
EXPIRED_INTERVAL = 60*60*24*7
WOOYUN_API_TYPE_CROP = 0
WOOYUN_API_TYPE_SUBMIT = 1



