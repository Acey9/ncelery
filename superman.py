#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    superman.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-01-25 18:01
#  Descrip :    
# -----------------------------------------------------
import socket
import copy
import sys
import os
#sys.path.append(os.sep.join(['../../..']))

from ncelery.config import conf as ncconf
from supervisord_conf import *
PROJECT = "ncelery"
CELERY_WORKDIR, _ = os.path.split(ncconf.PROJECT_PATH)
CONF_FILE_DIR, _ = os.path.split(SUPERVISORD_CONF)

conf_map = {}
print ncconf.APP_SUPERVISORD_CONF
for app_name, conf in ncconf.APP_SUPERVISORD_CONF.iteritems():
    conf_map.setdefault(app_name, {})
    node_num_key = app_name.upper()

    node_num = conf.get('node_num')
    concurrency = 1
    autoscale = ''#--autoscale=max, min
    pool = 'prefork'
    priority = 777

    if app_name == 'downloader':
        concurrency = 64 
        pool = 'eventlet'

    if app_name == 'phishing_hostcheck':
        concurrency = 64
        pool = 'eventlet'

    #to_var = '%s = %s ' % (node_num_key, node_num)
    #exec to_var

    parameter = {
            'node_num':node_num,
            'concurrency':concurrency,
            'autoscale':autoscale,
            'pool':pool,
            'priority':priority,
            }
    conf_map[app_name].update(parameter)

HOST_NAME = socket.gethostname()

GLOBAL_CONF = {
        'celery_user':CELERY_USER,
        'workdir':CELERY_WORKDIR,
        'celery_log_level':CELERY_LOG_LEVEL,
        'supervisor_user':SPVR_START_PROGRAM_USER,
        'supervisor_log':SPVR_PROGRAM_LOG_DIR,
        'project':PROJECT,
        'host_name':HOST_NAME,
        }

CMD = (
        "celery worker"
        " -A %(project)s"
        " -Q %(queue)s"
        " -c %(concurrency)s"
        " -l %(celery_log_level)s"
        " -n %(host_name)s.%%(program_name)s.%%(process_num)02d"
        " -P %(pool)s"
        " --workdir=%(workdir)s"
        " --uid=%(celery_user)s"
        " %(autoscale)s"
        " --without-mingle"
        " --without-gossip"
        #" --without-heartbeat"
        #" --autoreload"
        )

NIGHTSWATCH_CMD_CONF = {
        'node_num':1,
        'priority':666,#priority
        'worker_name':'nightswatch',
        'pidfile':NIGHTSWATCH_PID_FILE,
        }

BEAT_CMD_CONF = {
        'node_num':1,
        'priority':666,#priority
        'worker_name':'HeartThrobbing',
        'pidfile':BEAT_PID_FILE,
        }

BEAT_CMD = (
        "celery beat"
        " -A %(project)s"
        " -l %(celery_log_level)s"
        " --workdir=%(workdir)s"
        " --uid=%(celery_user)s"
        " --pidfile=%(pidfile)s"
        )

FILE = (
        "[program:%(worker_name)s]\n"
        "command = %(cmd)s\n\n"
        "environment = PYTHONPATH = %(workdir)s\n\n"               
        "directory = %(workdir)s\n"                            
        "user = %(supervisor_user)s\n"
        "process_name = %%(process_num)02d\n"        
        "numprocs = %(node_num)s\n"
        "stdout_logfile = %(supervisor_log)s\n"                       
        "stderr_logfile = %(supervisor_log)s\n"                       
        "autostart = false\n"                                         
        "autorestart = true\n"
        "startsecs = 3\n"
        "stopwaitsecs = 10\n"
        "priority = %(priority)s\n"
        )

supervisord_conf = {
        'sock':SPVR_SOCK,
        'port':SPVR_PORT,
        'admin':SPVR_ADMIN,
        'admin_password':SPVR_ADMIN_PASSWORD,
        'log_file':SPVR_LOG_FILE,
        'pid_file':SPVR_PID_FILE,
        'childlogdir':SPVR_CHILDLOGDIR,
        'default_user':SPVR_START_PROGRAM_USER,
        }

supervisord_file = (
        "[unix_http_server]\n"
        "file = %(sock)s\n\n"

        "[inet_http_server]\n"
        "port = 0.0.0.0:%(port)s\n"
        "username = %(admin)s\n"
        "password = %(admin_password)s\n\n"

        "[supervisord]\n"
        "logfile = %(log_file)s\n"
        "logfile_maxbytes = 50MB\n"
        "logfile_backups = 10\n"
        "loglevel = info\n"
        "pidfile = %(pid_file)s\n"
        "nodaemon = false\n"
        "minfds = 1024\n"
        "minprocs = 200\n"
        "user = %(default_user)s\n"
        "childlogdir = %(childlogdir)s\n\n"

        "[rpcinterface:supervisor]\n"
        "supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface\n"

        "[supervisorctl]\n"
        "serverurl = unix://%(sock)s\n\n"

        "[include]\n"
        "files = "
        )

def writeFile(path, data):
    print 'create file:', path
    fd = open(path, 'w')
    fd.write(data)
    fd.close()

class InvalidQueueName(Exception):
    pass

class Superman(object):

    app_switch = ncconf.APP_SUPERVISORD_CONF

    def getRoute(self, app_name):
        routes = self.app_switch.get(app_name, {}).get('routes', {}).values()
        if not routes:
            print 'WARNING, app name "%s", not routes.' % app_name
        reoute_name = [] 
        for route in routes:
            reoute_name.append(route.get('queue'))
        return list(set(reoute_name))

    def getAPPName(self, app, route):
        if route[:4] != 'ncq.':
            raise InvalidQueueName('Queue name not startswith \'ncq.\'')
        route = route[4:]
        #if route.startswith(app+'.'):
        #    return route
        #return '%s.%s' % (app, route)
        return route

    def getNameAndRoute(self, app):
        routes = self.getRoute(app)
        for route in routes:
            app_name = self.getAPPName(app, route)
            yield app_name, route

    def updateConf(self):
        for app in conf_map:
            try:
                node_num = conf_map[app].get('node_num')
                node_num = int(node_num)
            except:
                print 'WARNING, app name "%s", node_num is %s' % (app, node_num)
                continue
            if not int(conf_map[app].get('node_num')):
                continue
            for app_name, route in self.getNameAndRoute(app):
                conf_map[app].setdefault('workers', [])
                conf_map[app]['workers'].append((app_name, route))

    def generateCMD(self, conf):
        _conf = copy.deepcopy(conf)
        _conf.update(GLOBAL_CONF)
        workers = _conf.get('workers', [])
        for worker in workers:
            worker_name = worker[0]
            queue = worker[1]
            _conf['queue'] = queue
            if queue == 'ncq.nmapscan':# nmap scann
                _c = copy.deepcopy(_conf)
                _c['concurrency'] = 5
                cmd = CMD % _c
            else:
                cmd = CMD % _conf
            if queue == 'ncq.spider':
                cmd += ' --maxtasksperchild=%d' % SPIDER_PER_WORKER
            yield worker_name, cmd

    def generateFile(self, app, app_conf, worker_name, cmd):
        gconf = copy.deepcopy(GLOBAL_CONF)
        gconf['worker_name'] = worker_name
        gconf['cmd'] = cmd
        gconf['node_num'] = app_conf['node_num']
        gconf['priority'] = app_conf['priority']
        gconf['supervisor_log'] = os.path.join(SPVR_PROGRAM_LOG_DIR, worker_name + '.log')
        buf = FILE % gconf
        _dir = os.path.join(CONF_FILE_DIR, app)
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        path = os.path.join(_dir, worker_name + '.conf')
        writeFile(path, buf)
        return os.path.join(app, worker_name + '.conf')

    def generateBeatFile(self):
        app = 'heartbeat'
        gconf = copy.deepcopy(GLOBAL_CONF)
        gconf.update(BEAT_CMD_CONF)
        cmd = BEAT_CMD % gconf
        gconf['cmd'] = cmd 
        worker_name = gconf['worker_name']
        gconf['supervisor_log'] = os.path.join(SPVR_PROGRAM_LOG_DIR, worker_name + '.log')
        buf = FILE % gconf
        _dir = os.path.join(CONF_FILE_DIR, app)
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        path = os.path.join(_dir, worker_name + '.conf')
        writeFile(path, buf)
        return os.path.join(app, worker_name + '.conf')

    def generateNightswatchFile(self):
        app = 'nightswatch'
        gconf = copy.deepcopy(GLOBAL_CONF)
        gconf.update(NIGHTSWATCH_CMD_CONF)
        cmd = 'python %s/ncelery/nightswatch.py' % CELERY_WORKDIR
        gconf['cmd'] = cmd 
        worker_name = 'nightswatch'
        gconf['supervisor_log'] = os.path.join(SPVR_PROGRAM_LOG_DIR, worker_name + '.log')
        buf = FILE % gconf
        _dir = os.path.join(CONF_FILE_DIR, app)
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        path = os.path.join(_dir, worker_name + '.conf')
        writeFile(path, buf)
        return os.path.join(app, worker_name + '.conf')

    def generateSupervisorConf(self, include_files):
        files = " ".join(include_files)
        buf = supervisord_file % supervisord_conf
        buf = '%s%s' % (buf, files)
        path = os.path.join(CONF_FILE_DIR, 'supervisord.conf')
        writeFile(path, buf)

    def main(self):
        include_files = []
        for app, conf in conf_map.iteritems():
            for worker_name, cmd in self.generateCMD(conf):
                path = self.generateFile(app, conf, worker_name, cmd)
                include_files.append(path)
        if BEAT_IS_ON:
            path = self.generateBeatFile()
            include_files.append(path)
            path = self.generateNightswatchFile()
            include_files.append(path)
        self.generateSupervisorConf(include_files)

if __name__ == '__main__':
    man = Superman()
    man.updateConf()
    man.main()
