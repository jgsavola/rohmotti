#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import base64
import Cookie
import datetime
import time
import math

from db.Henkilo import Henkilo
from util import salasana
from util.sessio import Sessio
from util.html_parser import CommentHTMLParser
from basehandler import BaseHandler

class Handler(BaseHandler):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.sessio = self.conf['sessio']

        self.headers = []
        self.parameters = {}

    def get(self):
        status_message = ''

        self.headers.append('Content-Type: text/html; charset=UTF-8')


        status = self.form.getvalue('status')
        if status is None:
            if self.sessio is None:
                self.set_status('Käyttäjä ei ole kirjautunut.')
                return [ self.headers, self.parameters ]

            #
            # Tarkista, että sessio on validi.
            #
            henkilo = Henkilo.load_from_database(self.sessio.henkilo_id)

            if self.sessio.remote_addr != self.conf['effective_remote_addr']:
                self.set_status('Session ip-osoite ei täsmää käyttäjän ip-osoitteen kanssa!')
            elif henkilo is None:
                self.set_status('Session käyttäjää %d ei löydy tietokannasta!' % self.sessio.henkilo_id)
            else:
                self.set_status('Tuttu henkilö %s</p>' % (self.sessio))

            return [ self.headers, self.parameters ]
        else:
            if status == 'error':
                self.set_status('Virheellinen toiminto')
            elif status == 'logged_out':
                self.set_status('Uloskirjautuminen OK.')
            elif status == 'logged_in':
                self.set_status('Tervetuloa %d.' % (self.sessio.henkilo_id))
            elif status == 'password_mismatch':
                self.set_status('Salasanat eroavat!')
            elif status == 'missing_input':
                self.set_status('Anna tunnus ja salasana!')
            elif status == 'login_failed':
                self.set_status('Kirjautuminen epäonnistui')
            elif status == 'missing_newuser_input':
                self.set_status('Ole hyvä ja täytä kaikki kentät!')
            elif status == 'username_exists':
                self.set_status('Tunnus on jo käytössä!')
            elif status == 'welcome':
                self.set_status('Tunnus luotu, tervetuloa!')

            return [ self.headers, self.parameters ]

    def post(self):
        status = None

        action_input = self.form.getvalue("action")
        if action_input is None or (action_input != 'login' and action_input != 'logout' and action_input != 'newuser'):
            status = 'error'
        elif action_input == 'logout':
            status = self.handle_logout()
        elif action_input == 'login':
            status = self.handle_login()
        elif action_input == 'newuser':
            status = self.handle_newuser()

        self.redirect_after_post("%s?status=%s" % (self.conf['full_path'], status))

        return [ self.headers, self.parameters ]

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

        return 'logged_out'

    def handle_login(self):
        tunnus_input = self.form.getvalue("tunnus")
        salasana_input = self.form.getvalue("salasana")

        if tunnus_input is None or salasana_input is None:
            self.parameters = { 'status': '<p class="status"></p>' }

            return 'missing_input'

        henkilo_ids = Henkilo.load_ids(tunnus=tunnus_input)

        # blääh
        henkilo_id = None
        for i in henkilo_ids:
            henkilo_id = i
            break

        henkilo = Henkilo.load_from_database(henkilo_id)
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
                return 'logged_in'

        return 'login_failed'

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
            return 'missing_newuser_input'

        #
        # Siivoa tekstimuotoiset parameterit. Nimissä ja tunnuksissa
        # ei sallita mitään tageja.
        #
        parser = CommentHTMLParser(ok_tags=[])

        henkilon_nimi = parser.parse_string(henkilon_nimi_input)
        tunnus = parser.parse_string(tunnus_input)

        if salasana1_input != salasana2_input:
            return 'password_mismatch'

        henkilo_ids = Henkilo.load_ids(tunnus=tunnus)

        # blääh
        henkilo_id = None
        for i in henkilo_ids:
            henkilo_id = i
            break

        henkilo = None
        if henkilo_id is not None:
            henkilo = Henkilo.load_from_database(henkilo_id)
        if henkilo is not None:
            self.parameters = { 'status': '<p class="status">Tunnus "%s" on jo käytössä!</p>' % (tunnus) }
            return 'username_exists'

        #
        # Tehdään salasanasta hajautussumma.
        #
        salasana_hash = salasana.hash_password(salasana1_input)

        #
        # Tallennetaan henkilo tietokantaan
        #
        henkilo = Henkilo.new(nimi=henkilon_nimi, tunnus=tunnus, salasana=salasana_hash, omistajaa=None)

        #
        # Luo uusi istunto saman tien.
        #
        self.create_new_session(henkilo_id=henkilo.henkilo_id)

        self.parameters = { 'status': '<p class="status">Tunnus luotu, tervetuloa %s!</p>' % (tunnus) }

        return 'welcome'

    def create_new_session(self, henkilo_id):
        timestamp = int(math.floor(time.time()))
        self.sessio = Sessio(henkilo_id=henkilo_id, start_timestamp=timestamp, remote_addr=self.conf['effective_remote_addr'])
        self.headers.append(self.sessio.create_cookie().output())

    def set_status(self, status):
        self.parameters.update({ 'status': '<p class="status">%s</p>' % (status)})
