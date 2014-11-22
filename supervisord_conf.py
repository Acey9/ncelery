#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    supervisord_conf.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-11-22 15:02
#  Descrip :    
# -----------------------------------------------------

#celery configuration
CELERY_USER = "top"
CELERY_LOG_LEVEL = "INFO"
BEAT_IS_ON = False #是否开启celery beat
BEAT_PID_FILE = '/var/log/2ncelery/celery_beat.pid' #celery beat pid文件
NIGHTSWATCH_PID_FILE = '/var/log/2ncelery/nighitswatch.pid' #celery worker存活监控进程pid文件

#supervisor conf
SPVR_START_PROGRAM_USER = "root"
SPVR_PROGRAM_LOG_DIR = "/var/log/2supervisord/"
SPVR_SOCK = '/var/run/ncelery.supervisor.sock'
SPVR_PORT = 9999
SPVR_ADMIN = 'fan'
SPVR_ADMIN_PASSWORD = 'fan'
SPVR_LOG_FILE = '/var/log/2supervisord/supervisord.log'
SPVR_PID_FILE = '/var/run/2supervisord.pid'
SPVR_CHILDLOGDIR = '/var/log/2supervisord/'

#supervisord configuration file.
SUPERVISORD_CONF = '/etc/ncelery/supervisord/supervisord.conf'


