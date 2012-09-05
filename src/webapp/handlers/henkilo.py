#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
from db.Henkilo import Henkilo

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        headers = []
        headers.append('Content-Type: text/html; charset=UTF-8')

        parameters = {}

        henkilo_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            henkilo_id = m.group(1)

        if self.conf['request_method'] == 'GET':
            if henkilo_id is not None:
                henkilo = Henkilo.load_from_database(henkilo_id)

                kuva_link = ''
                for kommentti in henkilo.kommentit:
                    kuva_link += "<img src=\"%s/../../kuva/%d\" alt=\"%s\" />\n" % (
                        self.conf['request_uri'],
                        kommentti.kommentti_id,
                        cgi.escape(kommentti.teksti))

                parameters = { 'nimi': henkilo.nimi,
                               'henkilo_id': henkilo.henkilo_id,
                               'tunnus': henkilo.tunnus,
                               'kuva': kuva_link}
            else:
                henkilolista = "<ul class=\"henkilolista\">\n"
                for id in Henkilo.load_ids():
                    henkilo = Henkilo.load_from_database(id)
                    henkilolista += "<li class=\"henkilolista\"><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], henkilo.henkilo_id, cgi.escape(henkilo.nimi))
                henkilolista += "</ul>\n"
                parameters = {'henkilolista': henkilolista, 'status': ''}
        elif self.conf['request_method'] == 'POST':
            nimi = self.form.getvalue("nimi")

            henkilo = Henkilo.new(nimi=nimi)

            henkilolista = "<ul>\n"
            for id in Henkilo.load_ids():
                henkilo = Henkilo.load_from_database(id)
                henkilolista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], henkilo.henkilo_id, henkilo.henkilo_id, cgi.escape(henkilo.nimi))
            henkilolista += "</ul>\n"

            s = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], henkilo.henkilo_id, henkilo.henkilo_id)
            parameters = {'henkilolista': henkilolista, 'status': s}

        return [ headers, parameters ]
