#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    _requests.py
#  Author  :    wanghui@
#  Project :    PA
#  Date    :    2014-08-08 10:11
#  Descrip :    
# -----------------------------------------------------
import requests

class Request(object):

    headers = {
            'user-agent':('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/35.0.1916.153 Safari/537.36 Pandaria/1.0'),
            }
    timeout = 30

    @classmethod
    def get(cls, url, params={}):
        return requests.get(
                url,
                headers=Request.headers,
                timeout=Request.timeout,
                verify=False,
                params=params,
                )

    @classmethod
    def post(cls, url, data={}):
        return requests.post(
                url,
                headers=Request.headers,
                timeout=Request.timeout,
                verify=False,
                data=data,
                )

if __name__ == '__main__':
    url = 'http://www.soso.com'
    r = Request.get(url)
    print r.url, r.status_code
    #print r.text
