#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    api.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-11-23 23:41
#  Descrip :    
# -----------------------------------------------------
import os
import sys
sys.path.append(os.sep.join(['../../..']))
import unittest

from ncelery.tasks.wooyun.wooyun_api import WooYun 

class WooYunTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def test_getBugs(self):
        print 'test_getBugsByCorp...'
        with WooYun() as wy:
            d = wy.getBugs(1)
            self.assertTrue((type(d) == dict))

    def test_getBugDetail(self):
        print 'test_getBugDetail...'
        bugid = 21881
        with WooYun() as wy:
            d = wy.getBugDetail(bugid)
            print d
            self.assertTrue((type(d) == dict))

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

