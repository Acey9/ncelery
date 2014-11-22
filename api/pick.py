#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    pick.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-01-18 00:59
#  Descrip :    
# -----------------------------------------------------
import os
import sys
import shutil

ROOT = os.path.dirname(__file__)

TASK_FLAG = '@ncelery.task('
FUNCTION_FLAG = 'def '
CLASS_FLAG = 'class '

INIT_FILE = os.path.join(ROOT, '__init__.py')
CELERY_PY = os.path.join(ROOT, 'celery.py')
SETTINGS_PY = os.path.join(ROOT, 'conf.py')

FILE_HEAD = ('#!/usr/bin/env python\n'
        '# -*- coding: UTF-8 -*-\n'
        '\n'
        'from __future__ import absolute_import\n'
        'from celery import Task\n'
        'from %s.celery import ncelery')

class Picker(object):

    def __init__(self, source, pkg_name='ncelery'):
        self.pkg_name = pkg_name
        self.pkg_tmp_dir = os.path.join(ROOT, source)
        self.pkg_path = os.path.join(ROOT, self.pkg_name)

    def findTaskPy(self):
        cmd = 'find %s -name \'*.py\'' % self.pkg_tmp_dir
        pys = os.popen(cmd).readlines()
        for py in pys:
            grep_cmd = 'grep \"%s\" %s ' % (TASK_FLAG, os.path.join(ROOT, py))
            grep_res = os.popen(grep_cmd).read()
            if TASK_FLAG not in grep_res:
                continue
            yield py.strip()

    def copyInitFile(self, path):
        paths = path.split('/')
        path = ''
        for p in paths:
            path = os.path.join(path, p)
            if path == ROOT:
                continue
            shutil.copy(INIT_FILE, path)

    def copyTaskconfPy(self, src, dst):
        src_file = os.path.join(src, 'taskconf.py')
        dst_file = os.path.join(dst, 'taskconf.py')
        shutil.copy(src_file, dst_file)

    def touchFile(self, py, content):
        src_path, filename = os.path.split(py)
        dst_path = src_path[len(self.pkg_tmp_dir)+1:]
        dst_path = os.path.join(ROOT, '%s/%s' % (self.pkg_name, dst_path))
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
            self.copyInitFile(dst_path)
            self.copyTaskconfPy(src_path, dst_path)
        dst_full_path = '%s/%s' % (dst_path, filename)
        fd = open(dst_full_path, 'a+')
        fd.write(content)
        fd.close()
        #print '+++++\nfile:\t %s' % dst_full_path
        #print 'content:\n%s----' % content 

    def pickTask(self, py):
        fd = open(py, 'r')
        lines = fd.readlines()
        fd.close()
        head = FILE_HEAD % self.pkg_name
        buf = '%s\n\n' % head
        task_begin = False 
        for line in lines:
            l = line.strip()
            if l.startswith(CLASS_FLAG):
                buf = '%s%s' % (buf, line)
                buf = '%s    pass\n\n' % buf
                continue
            if l.startswith(TASK_FLAG):
                task_begin = True
            if not task_begin:
                continue
            buf = '%s%s' % (buf, line)
            if l.startswith(FUNCTION_FLAG):
                buf = '%s    pass\n\n' % buf
                task_begin = False
        return buf

    def clean(self):
        shutil.rmtree(self.pkg_path, ignore_errors=True)

    def pick(self):
        self.clean()
        for py in self.findTaskPy():
            buf = self.pickTask(py)
            self.touchFile(py, buf)

if __name__ == '__main__':
    src = sys.argv[1]
    pkg_name = sys.argv[2]

    p = Picker(src, pkg_name)
    p.pick()
