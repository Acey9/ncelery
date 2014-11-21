#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    nightswatch.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-04-13 14:35
#  Descrip :    
# -----------------------------------------------------
import socket
import subprocess
import json
import os
import time
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.utils import formatdate
from email.MIMEText import MIMEText

from .config import conf
from utils._requests import Request

MAIL = {
    'user':conf.SERVER_EMAIL,
    'passwd':conf.EMAIL_HOST_PASSWORD,
    'server':conf.EMAIL_HOST,
    'port':conf.EMAIL_PORT,
    'sender':conf.SERVER_EMAIL,
}

RECEIVER = [email for name, email in conf.ADMINS]

BROKER = conf.BROKER 

HOST_NAME = socket.gethostname()

path, _ = os.path.split(conf.CELERYBEAT_SCHEDULE_FILENAME)
data_file = path + '/nightswatch.db'

single_interval = 60
single_times = 60

class Dog(object):

    ping_cmd = "celery inspect ping  -b %s |grep celery |grep -v grep  |awk '{print $2}'" % BROKER

    def ping(self):
        sp = subprocess.Popen(self.ping_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ret = sp.wait()
        workers = []
        for line in sp.stdout.readlines():
            l = line.strip()[line.find('celery'):][:-1]
            workers.append(l)
        return workers

    def __call__(self):
        return self.ping()

class Checker(object):
    
    def lastCheck(self):
        if not os.path.isfile(data_file):
            return []
        f = open(data_file, 'r')
        buf = f.read()
        f.close()
        if buf:
            return json.loads(buf)
        return []

    def newCheck(self):
        return Dog()()

    def setLast(self, data):
        if not data:
            return
        f = open(data_file, 'w')
        f.write(json.dumps(data))
        f.close()

    def diff(self, new, last):
        add = filter(lambda x:x not in last, new)
        remove = filter(lambda x:x not in new, last)
        return add, remove

    def check(self):
        last = self.lastCheck()
        if not last:
            new = self.newCheck()
            self.setLast(new)
            return [], [] 

        check_result = {
                'add':{}, 
                'remove':{}
                }
        i = single_times
        while 1:
            print '%s check time:%s' % (time.asctime(), i)
            i -= 1
            if i < 0:
                break
            new = self.newCheck()
            add, remove = self.diff(new, last)
            for a in add:
                check_result['add'].setdefault(a, 0)
                check_result['add'][a] += 1
            for r in remove:
                check_result['remove'].setdefault(r, 0)
                check_result['remove'][r] += 1
            time.sleep(single_interval)

        adds = []
        for worker, count in check_result['add'].iteritems():
            if count < single_times:
                continue
            adds.append(worker)

        removes = []
        for worker, count in check_result['remove'].iteritems():
            if count < single_times:
                continue
            removes.append(worker)

        last = list(set(last) - set(removes))
        last.extend(adds)
        self.setLast(last)
        print 'add:', adds
        print 'remove:', removes
        return adds, removes

def sendMail(subject, content, emails, outfile=None):
    print 'send mail...'
    smtp = smtplib.SMTP(MAIL['server'], MAIL['port'])
    #smtp.starttls()
    #smtp.login(MAIL['user'].split('@')[0], MAIL['passwd'])
    msg = MIMEMultipart()
    msg['From'] = MAIL['sender']
    msg['Subject'] = subject
    msg['To'] = ','.join(emails)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(content,'html'))
    smtp.sendmail(MAIL['user'], emails, msg.as_string())

def killWorker(name):
    cmd = "ps ajx |grep \"%s\" |grep -v 'grep' |awk '{print $2}'|xargs kill -9" % name
    print '%s killWorker cmd:%s' % (time.asctime(), cmd)
    os.system(cmd)

def action(add, remove):
    print '%s action...' % time.asctime()
    content = ''
    subject = u"[Warning] Celery worker is Online. From night's watch %s" % HOST_NAME
    #for a in  add:
    #    if not a:
    #        continue
    #    content = '%s%s is Online<br>' % (content, a)
    for r in remove:
        if not r:
            continue
        if HOST_NAME in r:
            try:
                _, _, name = r.partition("@")
                killWorker(name)
                content = '%s%s is Offline. Has been executed kill -9.<br/>' % (content, r)
            except BaseException, e:
                print 'error:', e
        else:
            content = '%s%s is Offline<br/>' % (content, r)
        subject = u"[Warning] Nima, celery worker is Offline. From night's watch %s" % HOST_NAME
    if not content:
        return
    try:
        sendMail(subject, content, RECEIVER)
    except BaseException, e:
        print e

def check():
    ck = Checker()
    add, remove = ck.check()
    action(add, remove)

if __name__ == '__main__':
    check()
    #sendMail('subject', 'content', RECEIVER)
