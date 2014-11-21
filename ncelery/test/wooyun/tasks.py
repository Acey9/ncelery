#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    tasks.py
#  Author  :    wanghui@
#  Project :    PAMC V6.2.2
#  Date    :    2013-06-03 07:04
#  Descrip :    
# -----------------------------------------------------
import os
import sys
sys.path.append(os.sep.join(['../../..']))

import unittest
import time

from ncelery.tasks.wooyun.tasks import getBugs
from ncelery.tasks.wooyun.tasks import getBugDetail

class TaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls): 
        pass

    def test_getBugs(self):
        limit = 100
        t = getBugs.s(limit, alerted_bug=(79823, 1413590926)).apply_async()
        i = 0
        while 1:
            res = getBugs.AsyncResult(t.id)
            if i > 30:
                self.assertEqual(str(res.status), 'SUCCESS')
                return 'Timeout.'
            if res.ready():
                print 'stauts:', res.status
                print 'successful:', res.successful()
                print 'result:', type(res.result)
                self.assertEqual(str(res.status), 'SUCCESS')
                self.assertTrue((type(res.result) == dict))
                print res.result
                return res
            i += 1
            time.sleep(1)

    def test_getBugDetail(self):
        _id = 21881
        t = getBugDetail.s(_id).apply_async()
        i = 0
        while 1:
            res = getBugDetail.AsyncResult(t.id)
            if i > 30:
                self.assertEqual(str(res.status), 'SUCCESS')
                return 'Timeout.'
            if res.ready():
                print 'stauts:', res.status
                print 'successful:', res.successful()
                print 'result:', type(res.result)
                self.assertEqual(str(res.status), 'SUCCESS')
                self.assertTrue((type(res.result) == dict))
                print res.result
                return res
            i += 1
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
