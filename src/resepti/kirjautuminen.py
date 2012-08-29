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

        if os.environ['REQUEST_METHOD'] == 'GET':
            return { }
        elif os.environ['REQUEST_METHOD'] == 'POST':
            tunnus = self.form.getvalue("tunnus")
            salasana = self.form.getvalue("salasana")

            henkilo = Henkilo.load_from_database(tunnus=tunnus)
            if henkilo is None:
                return { 'status': '<p class="status">Tunnus "%s" on tuntematon<p>' % (cgi.escape(tunnus)) }

            if salasana == henkilo.salasana:
                return { 'status': '<p class="status">Tervetuloa, henkilö %d!</p>' % (henkilo.henkilo_id) }
                C = Cookie.SimpleCookie()
                C["henkilo_id"] = henkilo.henkilo_id

                sys.stdout.write("Content-Type: text/html; charset=UTF-8\r\n")
                sys.stdout.write(C.output())
                sys.stdout.write("\r\n\r\n")

            else:
                return { 'status': '<p class="status">Kirjautumisyritys hyvä, mutta ei riittävä!</p>' }
