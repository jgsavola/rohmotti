#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
from basehandler import BaseHandler
from db.Henkilo import Henkilo

class Handler(BaseHandler):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.headers = []
        self.parameters = {}

        self.henkilo_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.henkilo_id = m.group(1)

    def get(self):
        if self.henkilo_id is not None:
            henkilo = Henkilo.load_from_database(self.henkilo_id)

            kuva_link = ''
            for kommentti in henkilo.kommentit:
                kuva_link += "<img src=\"%s/../../kuva/%d\" alt=\"%s\" />\n" % (
                    self.conf['request_uri'],
                    kommentti.kommentti_id,
                    cgi.escape(kommentti.teksti))

            self.parameters.update({ 'nimi': henkilo.nimi,
                                'henkilo_id': henkilo.henkilo_id,
                                'tunnus': henkilo.tunnus,
                                'kuva': kuva_link})
        else:
            henkilolista = self.render_henkilolista()

            self.parameters.update({ 'henkilolista': henkilolista, 'status': '' })

        self.headers.append('Content-Type: text/html; charset=UTF-8')

        return [ self.headers, self.parameters ]

    def post(self):
        nimi = self.form.getvalue("nimi")

        henkilo = Henkilo.new(nimi=nimi)

        henkilolista = self.render_henkilolista()

        self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], henkilo.henkilo_id))
        return [ self.headers, self.parameters ]

    def render_henkilolista(self):
        henkilolista = "<ul class=\"henkilolista\">\n"
        for id in Henkilo.load_ids():
            henkilo = Henkilo.load_from_database(id)
            henkilolista += "<li class=\"henkilolista\"><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], henkilo.henkilo_id, cgi.escape(henkilo.nimi))
        henkilolista += "</ul>\n"

        return henkilolista
