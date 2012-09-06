#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseHandler(object):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.headers = []
        self.parameters = {}

    def handle(self):
        dispatch = { 'GET': self.get,
                     'POST': self.post,
                     'PUT': self.put,
                     'DELETE': self.delete
                     }
        return dispatch[self.conf['request_method']]()

    def get(self):
        return [ self.headers, self.parameters ]

    def post(self):
        return [ self.headers, self.parameters ]

    def delete(self):
        return [ self.headers, self.parameters ]

    def put(self):
        return [ self.headers, self.parameters ]

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))
