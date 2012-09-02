#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
from Ruokaaine import Ruokaaine
from Kommentti import Kommentti
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
        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        ruokaaine_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            ruokaaine_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            self.ruokaaine = Ruokaaine.load_from_database(ruokaaine_id = ruokaaine_id)

            self.render_page()

        return [ self.headers, self.parameters ]

    def render_page(self):
        kuva_link = ''
        for kommentti in self.ruokaaine.kommentit:
            kuva_link += "<div class=\"comment\">"
            kuva_link += "<div class=\"timestamp\">%s</div>\n" % (kommentti.aika)
            kuva_link += "<img src=\"%s/../../kuva/%d\" alt=\"%s\" />\n" % (
                self.conf['request_uri'],
                kommentti.kommentti_id,
                '')
            kuva_link += "<div class=\"commenttext\">%s</div>\n" % (kommentti.teksti)
            kuva_link += "</div>"

        status = ''
        if self.form.getvalue('updated', '') == 'true':
            status = '<p class="status">Tallennettu.</p>'
        elif self.form.getvalue('comment_created') is not None:
            status = '<p class="status">Uusi kommentti: %d</p>' % (int(self.form.getvalue('comment_created')))

        self.parameters.update({ 'nimi': cgi.escape(self.ruokaaine.nimi),
                                 'ruokaaine_id': self.ruokaaine.ruokaaine_id,
                                 'kuva': kuva_link,
                                 'status': status })
