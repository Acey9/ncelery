#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    setup.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-01-18 03:38
#  Descrip :    
# -----------------------------------------------------

from setuptools import setup, find_packages

setup(
        name = 'ncelery_api',
        version = '1.0',
        ext_package="ncelery",
        description = 'ncelery api.',
        author = 'wanghui',
        author_email = 'huiwang.e@gmail.com',
        packages = find_packages(),
        )

