# -*- coding: utf-8 -*-

import json
import time
import urllib
import requests


class Client(object):
    def __init__(self, api_host, api_port):
        # const define
        self.api_host = api_host
        self.api_port = api_port
        self.api_url = 'http://%s:%s' % (self.api_host, self.api_port)

        # init basic info
        self.session = requests.session()

    def _assert_error(self, d):
        if 'error_code' in d and 'error' in d:
            raise RuntimeError("[%s] %s" % (d['error_code'], d['error']))

    def get(self, uri, **kwargs):
        """
        Request resource by get method.
        """
        url = "%s%s" % (self.api_url, uri)
        res = json.loads(self.session.get(url, params=kwargs).text)

        self._assert_error(res)
        return res

    def post(self, uri, **kwargs):
        """
        Request resource by post method.
        """
        url = "%s%s.json" % (self.api_url, uri)
        res = json.loads(self.session.post(url, data=kwargs).text)
        self._assert_error(res)
        return res