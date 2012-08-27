#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
from Resepti import Resepti

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        path_info = os.environ.get('PATH_INFO', '')

        resepti_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            resepti_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            if resepti_id is not None:
                resepti = Resepti.load_from_database(resepti_id = resepti_id)

                kuva_link = ''
                for kommentti in resepti.kommentit:
                    kuva_link += "<img src=\"%s/../../kuva/%d\"/>\n" % (self.conf['request_uri'], kommentti.kommentti_id)

                return {'nimi': resepti.nimi, 'resepti_id': resepti.resepti_id, 'valmistusohje': resepti.valmistusohje, 'kuva': kuva_link}
            else:
                reseptilista = "<ul>\n"
                for id in Resepti.load_ids():
                    resepti = Resepti.load_from_database(id)
                    reseptilista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id, resepti.nimi)
                reseptilista += "</ul>\n"
                return {'reseptilista': reseptilista, 'status': ''}
        elif os.environ['REQUEST_METHOD'] == 'POST':
            nimi = self.form.getvalue("nimi")

            resepti = Resepti.new(nimi=nimi)

            reseptilista = "<ul>\n"
            for id in Resepti.load_ids():
                resepti = Resepti.load_from_database(id)
                reseptilista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id, resepti.nimi)
            reseptilista += "</ul>\n"

            s = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id)
            return {'reseptilista': reseptilista, 'status': s}
