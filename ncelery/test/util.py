#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    util.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-07-29 19:57
#  Descrip :    
# -----------------------------------------------------

import time

def asyncResult(task, task_id, timeout=30):
    i = 0
    while 1:
        res = task.AsyncResult(task_id)
        if i > timeout:
            break
        if res.ready():
            return res.status, res.result
        i += 1
        time.sleep(1)
    return 'timeout', ''

