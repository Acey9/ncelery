#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    taskconf.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-03-09 14:30
#  Descrip :    
# -----------------------------------------------------
from datetime import timedelta

###################include app########################

INCLUDE_APP = ['ncelery.tasks.example.tasks',]

###################tasks routes#######################
#Note: One module one queue
CELERY_ROUTES = {
        "ncelery.tasks.example.tasks.add":{
            "queue":"ncq.example"
            },
        }

CELERYBEAT_SCHEDULE = {
        'add-every-30-minute':{
            'task': 'ncelery.tasks.example.tasks.add',
            'schedule': timedelta(seconds=60*30),
            },
        }

######################celery annotations###############
#This setting can be used to rewrite any task attribute from the configuration.
#CELERY_ANNOTATIONS = {"*":{"time_limit":5, "soft_time_limit":3}}
CELERY_ANNOTATIONS = {
    #example
    "ncelery.tasks.example.tasks.add":{
        "time_limit":15, 
        "soft_time_limit":10,
        },
}


