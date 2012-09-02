#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import sys
import re
import psycopg2
import json
import cgi
from Resepti import Resepti
from ReseptiRuokaaine import ReseptiRuokaaine
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.sessio = self.conf['sessio']

        self.headers = []
        self.parameters = {}

        if os.environ['REQUEST_METHOD'] == 'GET':
            self.headers.append('Content-Type: text/html; charset=UTF-8')
            self.render_page()
        elif os.environ['REQUEST_METHOD'] == 'POST':
            nimi = self.form.getvalue("nimi")

            resepti = Resepti.new(nimi=nimi)

            self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], resepti.resepti_id))

        return [ self.headers, self.parameters ]

    def render_page(self):
        status = ''

        resepti_id_input = self.form.getvalue('inserted')
        if resepti_id_input is not None:
            resepti_id = int(resepti_id_input)
            status = ("<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['full_path'], resepti_id, resepti_id))

        reseptilista = "<ul class=\"reseptilista\">\n"
        for id in Resepti.load_ids():
            resepti = Resepti.load_from_database(id)
            reseptilista += "<li><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['full_path'], resepti.resepti_id, cgi.escape(resepti.nimi))
        reseptilista += "</ul>\n"

        self.parameters.update({ 'reseptilista': reseptilista, 'status': status })

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))
