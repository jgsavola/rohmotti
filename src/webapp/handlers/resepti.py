#!/usr/bin/python
# -*- coding: utf-8 -*- 

import cgi
from basehandler import BaseHandler
from db.Resepti import Resepti
from db.ReseptiRuokaaine import ReseptiRuokaaine
from util.html_parser import CommentHTMLParser

class Handler(BaseHandler):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.headers = []
        self.parameters = {}

        self.sessio = self.conf['sessio']

    def get(self):
        status = ''

        resepti_id_input = self.form.getvalue('inserted')
        if resepti_id_input is not None:
            resepti_id = int(resepti_id_input)
            status = ("<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['full_path'], resepti_id, resepti_id))

        resepti_id_input = self.form.getvalue('deleted')
        if resepti_id_input is not None:
            resepti_id = int(resepti_id_input)
            status = ("<p class=\"status\">Poistettu: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['full_path'], resepti_id, resepti_id))

        reseptilista = "<ul class=\"reseptilista\">\n"
        for id in Resepti.load_ids():
            resepti = Resepti.load_from_database(id)
            delete_form = """<form class="deleteform" action="%s/%d" method="post">
                               <input type="hidden" name="method_override" value="DELETE" />
                               <input type="submit" value="Poista" class="deleteform" />
                             </form>""" % (self.conf['full_path'], resepti.resepti_id)
            reseptilista += "<li><a href=\"%s/%d\">%s</a> %s</li>\n" % (self.conf['full_path'], resepti.resepti_id, cgi.escape(resepti.nimi), delete_form)
        reseptilista += "</ul>\n"

        self.headers.append('Content-Type: text/html; charset=UTF-8')
        self.parameters.update({ 'reseptilista': reseptilista, 'status': status })

        return [ self.headers, self.parameters ]

    def post(self):
        nimi = self.form.getvalue("nimi")

        resepti = Resepti.new(nimi=nimi)

        self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], resepti.resepti_id))

        return [ self.headers, self.parameters ]
