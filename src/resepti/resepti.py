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
from ReseptiRuokaaine import ReseptiRuokaaine
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        path_info = os.environ.get('PATH_INFO', '')

        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        if os.environ['REQUEST_METHOD'] == 'GET':
            self.render_page()
        elif os.environ['REQUEST_METHOD'] == 'POST':
            nimi = self.form.getvalue("nimi")

            resepti = Resepti.new(nimi=nimi)
            status = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id)

            self.render_page()

            self.parameters.update({ 'status': status })

        return [ self.headers, self.parameters ]

    def render_page(self):
        reseptilista = "<ul class=\"reseptilista\">\n"
        for id in Resepti.load_ids():
            resepti = Resepti.load_from_database(id)
            reseptilista += "<li><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], resepti.resepti_id, cgi.escape(resepti.nimi))
        reseptilista += "</ul>\n"

        self.parameters.update({ 'reseptilista': reseptilista, 'status': '' })
