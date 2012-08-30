#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
import Cookie

from Henkilo import Henkilo

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self._conf = conf

    @property
    def conf(self):
        """Get the configuration"""
        return self._conf

    def render(self):
        path_info = os.environ.get('PATH_INFO', '')

        headers = []
        headers.append('Content-Type: text/html; charset=UTF-8')

        parameters = {}

        if os.environ['REQUEST_METHOD'] == 'GET':
            C = Cookie.SimpleCookie()
            C.load(os.environ.get('HTTP_COOKIE'))
            try:
                henkilo_id = C["henkilo_id"]
                parameters = { 'status': '<p class="status">Tuttu henkilö %d</p>' % (int(henkilo_id.value)) }
            except KeyError:
                parameters = { 'status': '<p class="status">KeyError</p>' }
        elif os.environ['REQUEST_METHOD'] == 'POST':
            tunnus = self.form.getvalue("tunnus")
            salasana = self.form.getvalue("salasana")

            henkilo = Henkilo.load_from_database(tunnus=tunnus)
            if henkilo is None:
                parameters = { 'status': '<p class="status">Tunnus "%s" on tuntematon<p>' % (cgi.escape(tunnus)) }
            elif salasana == henkilo.salasana:
                parameters = { 'status': '<p class="status">Tervetuloa, henkilö %d!</p>' % (henkilo.henkilo_id) }

                C = Cookie.SimpleCookie()
                C["henkilo_id"] = henkilo.henkilo_id

                headers.append(C.output())
            else:
                parameters = { 'status': '<p class="status">Kirjautumisyritys hyvä, mutta ei riittävä!</p>' }

        return [ headers, parameters ]
