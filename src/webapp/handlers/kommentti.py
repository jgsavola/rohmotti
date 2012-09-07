#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Kommentti import Kommentti
from util.html_parser import CommentHTMLParser

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

        self.kohde_id = None
        m = re.match(r'/([^/]+)/(\d+)/kommentti(/(\d+))?', self.conf['path_info'])

        if m is None:
            return

        self.kohde_luokka = m.group(1)
        self.kohde_id = int(m.group(2))
        if self.kohde_luokka not in ['resepti', 'ruokaaine']:
            # error
            pass
        self.kommentti_id = None if m.group(4) is None else int(m.group(4))

    def post(self):
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

        if self.sessio is not None:
            kommentti.omistaja = self.sessio.henkilo_id
            kommentti.save()

        self.redirect_after_post("%s/%s/%d?comment_created=%d&yyy=%s" %
                                 (self.conf['script_name'],
                                  self.kohde_luokka,
                                  self.kohde_id,
                                  kommentti.kommentti_id,
                                  kuva is None))

        return [ self.headers, self.parameters ]

    def delete(self):
        if not self.authorized():
            self.redirect_after_post("%s/%s/%d?status=not_authorized" %
                                     (self.conf['script_name'],
                                      self.kohde_luokka,
                                      self.kohde_id))

            return [ self.headers, self.parameters ]
            
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
