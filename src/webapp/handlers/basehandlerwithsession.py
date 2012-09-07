#!/usr/bin/python
# -*- coding: utf-8 -*-

from basehandler import BaseHandler

class BaseHandlerWithSession(BaseHandler):
    def __init__(self, form, conf):
        super(BaseHandlerWithSession, self).__init__(form, conf)

        self.sessio = self.conf['sessio']

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

    def authorized(self, kohde_id=None):
        """Yksinkertaistettu auktorisointi: jos käyttäjä kirjautunut, salli; muuten: älä salli."""

        if self.sessio is None:
            return False

        return True
