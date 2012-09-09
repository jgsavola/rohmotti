#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Rajoitus import Rajoitus
from util.html_parser import CommentHTMLParser

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

        self.kohde_id = None
        m = re.match(r'/([^/]+)/(\d+)/rajoitus(/(\d+))?', self.conf['path_info'])

        if m is None:
            return

        self.kohde_luokka = m.group(1)
        self.kohde_id = int(m.group(2))
        if self.kohde_luokka not in ['henkilo']:
            # error
            pass
        self.rajoitus_id = None if m.group(4) is None else int(m.group(4))

    def post(self):
        rajoitus_input = self.form.getvalue('rajoitus')
        rajoitus = None

        if rajoitus_input is not None:
            parser = CommentHTMLParser(ok_tags=[])
            rajoitus = parser.parse_string(rajoitus_input)

        ruokaaine_id_input = self.form.getvalue('ruokaaine_id')
        if ruokaaine_id_input is not None:
            ruokaaine_id = int(ruokaaine_id_input)

        rajoitus = Rajoitus.new(henkilo_id=self.kohde_id,
                                ruokaaine_id=ruokaaine_id,
                                rajoitus=rajoitus)

        self.redirect_after_post("%s/%s/%d?rajoitus_created=%d" %
                                 (self.conf['script_name'],
                                  self.kohde_luokka,
                                  self.kohde_id,
                                  rajoitus.rajoitus_id))

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
