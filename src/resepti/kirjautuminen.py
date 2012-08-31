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
        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        C = Cookie.SimpleCookie()
        C.load(os.environ.get('HTTP_COOKIE', ''))
        self.sessio = Sessio.new_from_cookie(C)

        if os.environ['REQUEST_METHOD'] == 'GET':
            self.handle_get()
        elif os.environ['REQUEST_METHOD'] == 'POST':
            self.handle_post()

        return [ self.headers, self.parameters ]

    def handle_get(self):
        if self.sessio is None:
            self.parameters = { 'status': '<p class="status">Käyttäjä ei ole kirjautunut.</p>' }
            return True

        #
        # Tarkista, että sessio on validi.
        #
        henkilo = Henkilo.load_from_database(self.sessio.henkilo_id)

        if self.sessio.remote_addr != self.conf['effective_remote_addr']:
            self.parameters = { 'status': '<p class="status">Session ip-osoite ei täsmää käyttäjän ip-osoitteen kanssa!</p><pre>%s</pre>' % (cgi.escape(str(self.sessio))) }
        elif henkilo is None:
            self.parameters = { 'status': '<p class="status">Session käyttäjää %d ei löydy tietokannasta!</p>' % (self.sessio.henkilo_id) }
        else:
            self.parameters = { 'status': '<p class="status">Tuttu henkilö %s</p>' % (self.sessio) }

        return True

    def handle_post(self):
        action_input = self.form.getvalue("action")
        if action_input is None or (action_input != 'login' and action_input != 'logout'):
            self.parameters = { 'status': '<p class="status">Virheellinen toiminto.</p>' }
            return True

        if action_input == 'logout':
            if self.sessio is None:
                #
                # Istuntoa ei ole, ei tehdä mitään.
                #
                self.parameters = { 'status': '<p class="status">OK</p>' }
                return True

            C = self.sessio.delete_cookie()
            self.headers.append(C.output())
            self.parameters = { 'status': '<p class="status">Uloskirjautuminen tehty.</p>' }

            return True
        elif action_input == 'login':
            tunnus_input = self.form.getvalue("tunnus")
            salasana_input = self.form.getvalue("salasana")

            if tunnus_input is None or salasana_input is None:
                self.parameters = { 'status': '<p class="status">Anna tunnus ja salasana!</p>' }

                return True

            henkilo = Henkilo.load_from_database(tunnus=tunnus_input)
            if henkilo is not None:
                #
                # Ota suola tietokannassa olevasta salasanasta ja aja
                # hajautusfunktion läpi.
                #
                suola = salasana.get_salt_from_hash(henkilo.salasana)
                salasana_hash = salasana.hash_password(salasana_input, suola)
                if salasana_hash == henkilo.salasana:
                    self.parameters = { 'status': '<p class="status">Tervetuloa, henkilö %d!</p>' % (henkilo.henkilo_id) }

                    timestamp = int(math.floor(time.time()))

                    self.sessio = Sessio(henkilo_id=henkilo.henkilo_id, start_timestamp=timestamp, remote_addr=self.conf['effective_remote_addr'])
                    self.headers.append(self.sessio.create_cookie().output())

                    #
                    # Kaikki OK!
                    #
                    return True

            self.parameters = { 'status': '<p class="status">Kirjautumisyritys hyvä, mutta ei riittävä!</p>' }

        return True
