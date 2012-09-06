#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cgi
from basehandler import BaseHandler
from db.Ruokaaine import Ruokaaine
from db.Resepti import Resepti
from db.ReseptiRuokaaine import ReseptiRuokaaine
from util.html_parser import CommentHTMLParser

class Handler(BaseHandler):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.headers = []
        self.parameters = {}

        self.kohde_id = None
        m = re.match(r'/resepti/(\d+)/ruokaaine(/(\d+))?', self.conf['path_info'])

        if m is not None:
            self.resepti_id = int(m.group(1))
            self.ruokaaine_id = None if m.group(3) is None else int(m.group(3))

    def post(self):
        ruokaaine_id_input = self.form.getvalue('ruokaaine_id')
        maara_input = self.form.getvalue('maara')
        mittayksikko_input = self.form.getvalue('mittayksikko')

        jarjestys = 42

        resepti = Resepti.load_from_database(self.resepti_id)
        ruokaaine = Ruokaaine.load_from_database(int(ruokaaine_id_input))

        reseptiruokaaine = ReseptiRuokaaine.new(resepti, ruokaaine, jarjestys, maara_input, mittayksikko_input)

        self.redirect_after_post("%s/resepti/%d?added=%d" %
                                 (self.conf['script_name'],
                                  self.resepti_id,
                                  reseptiruokaaine.ruokaaine.ruokaaine_id))

        return [ self.headers, self.parameters ]

    def delete(self):
        #
        # Salli DELETE vain yksittäisille kommenteille. Jos
        # reseptiruokaaine_id:tä ei ole määritelty polussa, olisi DELETE
        # tulkittava niin, että kaikki reseptin kommentit halutaan
        # hävittää.
        #
        if self.reseptiruokaaine_id is not None:
            ReseptiRuokaaine.delete(reseptiruokaaine_id=self.reseptiruokaaine_id)

            self.redirect_after_post("%s/%s/%d?comment_deleted=%d" %
                                     (self.conf['script_name'],
                                      self.kohde_luokka,
                                      self.resepti_id,
                                      self.reseptiruokaaine_id))


        return [ self.headers, self.parameters ]
