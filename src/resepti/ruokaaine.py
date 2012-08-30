#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
from Ruokaaine import Ruokaaine

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

        ruokaaine_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            ruokaaine_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            if ruokaaine_id is not None:
                ruokaaine = Ruokaaine.load_from_database(ruokaaine_id = ruokaaine_id)

                kuva_link = ''
                for kommentti in ruokaaine.kommentit:
                    kuva_link += "<img src=\"%s/../../kuva/%d\" alt=\"%s\" />\n" % (
                        self.conf['request_uri'],
                        kommentti.kommentti_id,
                        cgi.escape(kommentti.teksti))

                parameters = {'nimi': ruokaaine.nimi, 'ruokaaine_id': ruokaaine.ruokaaine_id, 'kuva': kuva_link}
            else:
                ruokaainelista = "<ul class=\"ruokaainelista\">\n"
                for id in Ruokaaine.load_ids():
                    ruokaaine = Ruokaaine.load_from_database(id)
                    ruokaainelista += "<li class=\"ruokaainelista\"><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, cgi.escape(ruokaaine.nimi))
                ruokaainelista += "</ul>\n"
                parameters = {'ruokaainelista': ruokaainelista, 'status': ''}
        elif os.environ['REQUEST_METHOD'] == 'POST':
            nimi = self.form.getvalue("nimi")

            ruokaaine = Ruokaaine.new(nimi=nimi)

            ruokaainelista = "<ul>\n"
            for id in Ruokaaine.load_ids():
                ruokaaine = Ruokaaine.load_from_database(id)
                ruokaainelista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, ruokaaine.ruokaaine_id, cgi.escape(ruokaaine.nimi))
            ruokaainelista += "</ul>\n"

            s = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, ruokaaine.ruokaaine_id)
            parameters = {'ruokaainelista': ruokaainelista, 'status': s}

        return [ headers, parameters ]
