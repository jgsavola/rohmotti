#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import psycopg2
import json
import cgi
import textwrap
from Resepti import Resepti
from Ruokaaine import Ruokaaine
from ReseptiRuokaaine import ReseptiRuokaaine
from Kommentti import Kommentti
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.headers = []
        self.parameters = {}

        self.kohde_id = None
        m = re.match(r'/([^/]+)/(\d+)/kommentti', self.conf['path_info'])

        if m is None:
            return

        self.kohde_luokka = m.group(1)
        self.kohde_id = int(m.group(2))
        if self.kohde_luokka not in ['resepti', 'ruokaaine']:
            # error
            return

        if os.environ['REQUEST_METHOD'] == 'GET':
            pass
        elif os.environ['REQUEST_METHOD'] == 'POST':
            teksti_input = self.form.getvalue('teksti')
            teksti = None

            if teksti_input is not None:
                parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                teksti = parser.parse_string(teksti_input)

            kuva_input = self.form.getvalue('kuva')

            kommentti = Kommentti.new(self.kohde_id, teksti, kuva_input)

            self.redirect_after_post("%s/%s/%d?comment_created=%d" %
                                     (self.conf['script_name'],
                                      self.kohde_luokka,
                                      self.kohde_id,
                                      kommentti.kommentti_id))

        return [ self.headers, self.parameters ]

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))
