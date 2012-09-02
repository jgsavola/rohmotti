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

        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        if self.conf['request_method'] == 'GET':
            self.render_page()
        elif self.conf['request_method'] == 'POST':
            nimi = self.form.getvalue("nimi")

            ruokaaine = Ruokaaine.new(nimi=nimi)
            status = ("<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['request_uri'],
                       ruokaaine.ruokaaine_id,
                       ruokaaine.ruokaaine_id))

            self.render_page()

            self.parameters.update({ 'status': status })

        return [ self.headers, self.parameters ]

    def render_page(self):
        ruokaainelista = "<ul class=\"ruokaainelista\">\n"
        for id in Ruokaaine.load_ids():
            ruokaaine = Ruokaaine.load_from_database(id)
            ruokaainelista += ("""<li class="ruokaainelista">
                                  <a href="%s/%d">%s</a></li> """ %
                               (self.conf['request_uri'],
                                ruokaaine.ruokaaine_id,
                                cgi.escape(ruokaaine.nimi)))
        ruokaainelista += "</ul>\n"

        self.parameters.update({'ruokaainelista': ruokaainelista, 'status': ''})
