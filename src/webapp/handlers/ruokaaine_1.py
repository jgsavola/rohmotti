#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
from db.Ruokaaine import Ruokaaine
from db.Kommentti import Kommentti
from util.html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.headers = []

        self.parameters = {}

        ruokaaine_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            ruokaaine_id = int(m.group(1))

        if self.conf['request_method'] == 'GET':
            self.headers.append('Content-Type: text/html; charset=UTF-8')

            self.ruokaaine = Ruokaaine.load_from_database(ruokaaine_id = ruokaaine_id)
            self.render_page()
        elif self.conf['request_method'] == 'DELETE':
            Ruokaaine.delete(ruokaaine_id=ruokaaine_id)

            self.redirect_after_post("%s/ruokaaine?deleted=%d" % (self.conf['script_name'], ruokaaine_id))

        return [ self.headers, self.parameters ]

    def render_page(self):
        kuva_link = ''
        for kommentti in self.ruokaaine.kommentit:
            delete_form = """<form class="deleteform" action="%s/kommentti/%d" method="post">
                               <input type="hidden" name="method_override" value="DELETE" />
                               <input type="submit" value="Poista" class="deleteform" />
                             </form>""" % (self.conf['full_path'], kommentti.kommentti_id)

            kuva_link += "<div class=\"comment\">"
            kuva_link += "<div class=\"timestamp\">%s %s</div>\n" % (kommentti.aika, delete_form)
            kuva_link += "<img src=\"%s/kuva/%d\" alt=\"%s\" />\n" % (
                self.conf['script_name'],
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

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))