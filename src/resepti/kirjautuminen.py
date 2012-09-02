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
from sessio import Sessio
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self._conf = conf

    @property
    def conf(self):
        """Get the configuration"""
        return self._conf

    def render(self):
        self.sessio = self.conf['sessio']

        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        if self.conf['request_method'] == 'GET':
            self.handle_get()
        elif self.conf['request_method'] == 'POST':
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
        if action_input is None or (action_input != 'login' and action_input != 'logout' and action_input != 'newuser'):
            self.parameters = { 'status': '<p class="status">Virheellinen toiminto.</p>' }
            return True

        if action_input == 'logout':
            return self.handle_logout()
        elif action_input == 'login':
            return self.handle_login()
        elif action_input == 'newuser':
            return self.handle_newuser()

        return True

    def handle_logout(self):
        if self.sessio is None:
            #
            # Istuntoa ei ole, ei tehdä mitään.
            #
            self.parameters = { 'status': '<p class="status">OK</p>' }
        else:
            #
            # Istunto on olemassa, palautetaan evästeenpoistoeväste.
            #
            C = self.sessio.delete_cookie()
            self.headers.append(C.output())
            self.parameters = { 'status': '<p class="status">Uloskirjautuminen tehty.</p>' }

        return True

    def handle_login(self):
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

    def handle_newuser(self):
        henkilon_nimi_input = self.form.getvalue("henkilon_nimi")
        tunnus_input = self.form.getvalue("tunnus")
        salasana1_input = self.form.getvalue("salasana1")
        salasana2_input = self.form.getvalue("salasana2")

        if (henkilon_nimi_input is None or
            tunnus_input is None or
            salasana1_input is None or
            salasana2_input is None):
            self.parameters = { 'status': '<p class="status">Ole hyvä ja täytä kaikki kentät!</p>' }

            return True

        #
        # Siivoa tekstimuotoiset parameterit. Nimissä ja tunnuksissa
        # ei sallita mitään tageja.
        #
        parser = CommentHTMLParser(ok_tags=[])

        henkilon_nimi = parser.parse_string(henkilon_nimi_input)
        tunnus = parser.parse_string(tunnus_input)

        if salasana1_input != salasana2_input:
            self.parameters = { 'status': '<p class="status">Salasanat eroavat!</p>' }
            return True

        henkilo = Henkilo.load_from_database(tunnus=tunnus)
        if henkilo is not None:
            self.parameters = { 'status': '<p class="status">Tunnus "%s" on jo käytössä!</p>' % (tunnus) }
            return True

        #
        # Tehdään salasanasta hajautussumma.
        #
        salasana_hash = salasana.hash_password(salasana1_input)

        #
        # Tallennetaan henkilo tietokantaan
        #
        henkilo = Henkilo.new(nimi=henkilon_nimi, tunnus=tunnus, salasana=salasana_hash)

        #
        # Luo uusi istunto saman tien.
        #
        self.create_new_session(henkilo_id=henkilo.henkilo_id)

        self.parameters = { 'status': '<p class="status">Tunnus luotu, tervetuloa %s!</p>' % (tunnus) }
        return True

    def create_new_session(self, henkilo_id):
        timestamp = int(math.floor(time.time()))
        self.sessio = Sessio(henkilo_id=henkilo_id, start_timestamp=timestamp, remote_addr=self.conf['effective_remote_addr'])
        self.headers.append(self.sessio.create_cookie().output())
