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

from celery import group, chord, chain
from ncelery.tasks.example.tasks import add, _link, _chord

class TaskTestCase(unittest.TestCase):

    url = 'http://www.so.com'
    url2 = 'https://github.com'

    @classmethod
    def setUpClass(cls): 
        pass

    def test_group_add(self):
        print 'test_group_add...'
        job = group(add.s(1, 2),
                add.s(3, 4),
                add.s(5, 6)
                )
        r = job.apply_async()
        print r.get()

    def test_chord_add(self):
        print 'test_chord_add...'
        job = group(add.s(1, 2),
                add.s(3, 4),
                add.s(5, 6)
                )
        r = chord(job)(_link.s(1))

    def test_chain_add2(self):
        print 'test_chain_add...'
        job = chain(add.s(1, 2),
                add.s(3),
                add.s(4)
                )
        r = job.apply_async()
        print r.get()

    def test_chord(self):
        r = _chord.s().apply_async()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
