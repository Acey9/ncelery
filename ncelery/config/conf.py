#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    conf.py
#  Author  :    wanghui@
#  Project :    ncelery
#  Date    :    2013-06-03
#  Descrip :    
# -----------------------------------------------------
import os

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_PATH, _ = os.path.split(CURRENT_DIR)

"""celery configuration"""
#Name of the main module if running
MAIN_NAME = "Pandaria"

#URL of the default broker used
BROKER = 'amqp://guest@espp.broker.com:5672//'

#The result store backend class, or the name of the backend class to use
BACKEND = 'redis://espp.redis.com:6379/1'

#include app
INCLUDE_APP = []

#tasks routes
#Note: One module one queue
CELERY_ROUTES = {}

#Periodic Tasks
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {}
CELERYBEAT_SCHEDULE_FILENAME = '/var/log/2ncelery/beat-schedule'

#This setting can be used to rewrite any task attribute from the configuration.
#CELERY_ANNOTATIONS = {"*":{"time_limit":5, "soft_time_limit":3}}
CELERY_ANNOTATIONS = {}

#app switch conf
APP_MODE_NUM = {
        #example
        'ncelery.tasks.example':1,
        }
EMD_PHISHING_NUM = 1
SCREENSHOT_PHISHING_NUM = 1

APP_SUPERVISORD_CONF = {}

IS_NCELERY_API = False 
for module, node_num in APP_MODE_NUM.iteritems():
    if not IS_NCELERY_API and not node_num:
        continue

    import_str = 'from %s import taskconf' % module
    exec import_str

    INCLUDE_APP.extend(taskconf.INCLUDE_APP)

    CELERY_ROUTES.update(taskconf.CELERY_ROUTES)

    CELERYBEAT_SCHEDULE.update(taskconf.CELERYBEAT_SCHEDULE)

    CELERY_ANNOTATIONS.update(taskconf.CELERY_ANNOTATIONS)

    APP_SUPERVISORD_CONF.setdefault(module, {})
    _conf = {'routes':taskconf.CELERY_ROUTES, 'node_num':node_num}
    APP_SUPERVISORD_CONF[module].update(_conf)

#ack late
CELERY_ACKS_LATE = True

#Tasks settings
CELERY_DEFAULT_QUEUE = "celery"

#result settings
CELERY_TASK_RESULT_EXPIRES = 60*15
CELERY_IGNORE_RESULT = True

#worker settings
#Maximum number of tasks a pool worker process can execute before it’s replaced with a new one.
CELERYD_MAX_TASKS_PER_CHILD = 128
#The number of concurrent worker processes/threads/green threads executing tasks.
CELERYD_CONCURRENCY = 1
#How many messages to prefetch at a time multiplied by the number of concurrent processes
CELERYD_PREFETCH_MULTIPLIER = 4

#Task hard time limit in seconds. The worker processing the task will be killed and replaced 
#with a new one when this is exceeded.
CELERYD_TASK_TIME_LIMIT = 60*6

#Task soft time limit in seconds.
#The SoftTimeLimitExceeded exception will be raised when this is exceeded. 
#The task can catch this to e.g. clean up before the hard time limit comes.
CELERYD_TASK_SOFT_TIME_LIMIT = 60*5

#Maximum number of connections available in the Redis connection pool used for sending and retrieving results.
CELERY_REDIS_MAX_CONNECTIONS = 128

#The maximum number of connections that can be open in the connection pool.
BROKER_POOL_LIMIT = 10
CELERYD_POOL_RESTARTS = True

#Send events so the worker can be monitored by tools like celerymon.
CELERY_SEND_EVENTS = False

#If enabled, a task-sent event will be sent for every task so tasks can be 
#tracked before they are consumed by a worker.
CELERY_SEND_TASK_SENT_EVENT = False

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = False
#Name and email addresses of recipients
#List of (name, email_address) tuples for the administrators that should receive error emails.
ADMINS = (
    ('wanghui', 'wanghui@xx.com'),
)
#Email address used as sender (From field).
SERVER_EMAIL = 'nightswatch@xx.com'
#Mailserver configuration
EMAIL_HOST = '10.7.254.150'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'nightswatch'
EMAIL_HOST_PASSWORD = ''
#Timeout in seconds for when we give up trying to connect to the SMTP server when sending emails.
EMAIL_TIMEOUT = 5
#Use SSL when connecting to the SMTP server.
EMAIL_USE_SSL = False
#Use TLS when connecting to the SMTP server. 
EMAIL_USE_TLS = False

#logging
LOGGING_CONFIG_FILE = os.path.normpath(os.path.join(PROJECT_PATH, 'config/logging.cfg'))
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

