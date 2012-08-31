#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
import base64
import Cookie
import datetime
import time
import math

from Henkilo import Henkilo
import salasana
from salaus import Salaus
from sessio import Sessio

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self._conf = conf

        self.secret_key = '2M\x93\x9a \x9d\x86zV\x04\xf3?\x08\x8a\xba7'
        self.salaus = Salaus(self.secret_key)

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
            C.load(os.environ.get('HTTP_COOKIE', ''))
            sessio = Sessio.new_from_cookie(C)

            if sessio is not None:
                if self.form.getvalue('logout') is not None:
                    C['rohmotti']['expires'] = 0
                    parameters = { 'status': '<p class="status">Uloskirjautuminen tehty.</p>' }
                    headers.append(C.output())

                    return [ headers, parameters ]

                #
                # Tarkista, että sessio on validi.
                #
                henkilo = Henkilo.load_from_database(sessio.henkilo_id)

                if sessio.remote_addr != self.conf['effective_remote_addr']:
                    parameters = { 'status': '<p class="status">Session ip-osoite ei täsmää käyttäjän ip-osoitteen kanssa!</p><pre>%s</pre>' % (str(sessio)) }
                elif henkilo is None:
                    parameters = { 'status': '<p class="status">Session käyttäjää %d ei löydy tietokannasta!</p>' % (sessio.henkilo_id) }
                else:
                    parameters = { 'status': '<p class="status">Tuttu henkilö %s</p>' % (sessio) }
        elif os.environ['REQUEST_METHOD'] == 'POST':
            tunnus_input = self.form.getvalue("tunnus")
            salasana_input = self.form.getvalue("salasana")

            if tunnus_input is None or salasana_input is None:
                parameters = { 'status': '<p class="status">Anna tunnus ja salasana!</p>' }
                return [ headers, parameters ]

            henkilo = Henkilo.load_from_database(tunnus=tunnus_input)
            if henkilo is not None:
                #
                # Ota suola tietokannassa olevasta salasanasta ja aja
                # hajautusfunktion läpi.
                #
                suola = salasana.get_salt_from_hash(henkilo.salasana)
                salasana_hash = salasana.hash_password(salasana_input, suola)
                if salasana_hash == henkilo.salasana:
                    parameters = { 'status': '<p class="status">Tervetuloa, henkilö %d!</p>' % (henkilo.henkilo_id) }

                    timestamp = int(math.floor(time.time()))

                    sessio = Sessio(henkilo_id=henkilo.henkilo_id, start_timestamp=timestamp, remote_addr=self.conf['effective_remote_addr'])
                    headers.append(sessio.create_cookie().output())

                    #
                    # Kaikki OK!
                    #
                    return [ headers, parameters ]

            parameters = { 'status': '<p class="status">Kirjautumisyritys hyvä, mutta ei riittävä!</p>' }

        return [ headers, parameters ]
