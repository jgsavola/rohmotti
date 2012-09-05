#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cgi
from db.Kommentti import Kommentti
from util.html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.headers = []
        self.parameters = {}

        self.kohde_id = None
        m = re.match(r'/([^/]+)/(\d+)/kommentti(/(\d+))?', self.conf['path_info'])

        if m is None:
            return

        self.kohde_luokka = m.group(1)
        self.kohde_id = int(m.group(2))
        if self.kohde_luokka not in ['resepti', 'ruokaaine']:
            # error
            return
        self.kommentti_id = None if m.group(4) is None else int(m.group(4))

        if self.conf['request_method'] == 'GET':
            pass
        elif self.conf['request_method'] == 'POST':
            teksti_input = self.form.getvalue('teksti')
            teksti = None

            if teksti_input is not None:
                parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                teksti = parser.parse_string(teksti_input)

            kuva_input = self.form.getvalue('kuva')
            kuva = None
            if kuva_input is not None and len(kuva_input) > 0:
                kuva = kuva_input

            kommentti = Kommentti.new(kohde_id=self.kohde_id, teksti=teksti, kuva=kuva)

            self.redirect_after_post("%s/%s/%d?comment_created=%d" %
                                     (self.conf['script_name'],
                                      self.kohde_luokka,
                                      self.kohde_id,
                                      kommentti.kommentti_id))
        elif self.conf['request_method'] == 'DELETE':
            #
            # Salli DELETE vain yksittäisille kommenteille. Jos
            # kommentti_id:tä ei ole määritelty polussa, olisi DELETE
            # tulkittava niin, että kaikki reseptin kommentit halutaan
            # hävittää.
            #
            if self.kommentti_id is not None:
                Kommentti.delete(self.kommentti_id)

                self.redirect_after_post("%s/%s/%d?comment_deleted=%d" %
                                         (self.conf['script_name'],
                                          self.kohde_luokka,
                                          self.kohde_id,
                                          self.kommentti_id))


        return [ self.headers, self.parameters ]

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))
