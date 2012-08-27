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
        self.conf = conf

    def render(self):
        path_info = os.environ.get('PATH_INFO', '')

        ruokaaine_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            ruokaaine_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            if ruokaaine_id is not None:
                ruokaaine = Ruokaaine.load_from_database(ruokaaine_id = ruokaaine_id)

                kuva_link = ''
                for kommentti in ruokaaine.kommentit:
                    kuva_link += "<img src=\"%s/../../kuva/%d\"/>\n" % (self.conf['request_uri'], kommentti.kommentti_id)

                return {'nimi': ruokaaine.nimi, 'ruokaaine_id': ruokaaine.ruokaaine_id, 'kuva': kuva_link}
            else:
                ruokaainelista = "<ul>\n"
                for id in Ruokaaine.load_ids():
                    ruokaaine = Ruokaaine.load_from_database(id)
                    ruokaainelista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, ruokaaine.ruokaaine_id, ruokaaine.nimi)
                ruokaainelista += "</ul>\n"
                return {'ruokaainelista': ruokaainelista, 'status': ''}
        elif os.environ['REQUEST_METHOD'] == 'POST':
            nimi = self.form.getvalue("nimi")

            ruokaaine = Ruokaaine.new(nimi=nimi)

            ruokaainelista = "<ul>\n"
            for id in Ruokaaine.load_ids():
                ruokaaine = Ruokaaine.load_from_database(id)
                ruokaainelista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, ruokaaine.ruokaaine_id, ruokaaine.nimi)
            ruokaainelista += "</ul>\n"

            s = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], ruokaaine.ruokaaine_id, ruokaaine.ruokaaine_id)
            return {'ruokaainelista': ruokaainelista, 'status': s}
