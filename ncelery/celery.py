#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    celery.py
#  Author  :    wanghui@
#  Project :    ncelery
#  Date    :    2013-06-03
#  Descrip :    
# -----------------------------------------------------
from __future__ import absolute_import

from logging.config import fileConfig
from celery.utils.log import get_task_logger
from celery import Celery
from .config import conf

get_task_logger = get_task_logger

ncelery = Celery(conf.MAIN_NAME, 
    broker=conf.BROKER,
    backend=conf.BACKEND, 
    include=conf.INCLUDE_APP
)

ncelery.config_from_object(conf)
fileConfig(conf.LOGGING_CONFIG_FILE)

if __name__ == '__main__':
    ncelery.start()
