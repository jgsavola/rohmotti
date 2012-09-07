#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Ruokaaine import Ruokaaine
from db.Kommentti import Kommentti
from db.Henkilo import Henkilo
from util.html_parser import CommentHTMLParser

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

        self.ruokaaine_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.ruokaaine_id = int(m.group(1))

    def get(self):
        self.ruokaaine = Ruokaaine.load_from_database(self.ruokaaine_id)

        kuva_link = ''
        for kommentti in self.ruokaaine.kommentit:
            tunnus = '<span class="tuntematon">tuntematon</span>'
            if kommentti.omistaja is not None:
                omistaja = Henkilo.load_from_database(kommentti.omistaja)
                tunnus = omistaja.tunnus

            delete_form = """<form class="deleteform" action="%s/kommentti/%d" method="post">
                               <input type="hidden" name="method_override" value="DELETE" />
                               <input type="submit" value="Poista" class="deleteform" />
                             </form>""" % (self.conf['full_path'], kommentti.kommentti_id)

            kuva_link += "<div class=\"comment\">"
            kuva_link += "<div class=\"timestamp\">%s %s %s</div>\n" % (tunnus, kommentti.aika, delete_form)
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

        self.headers.append('Content-Type: text/html; charset=UTF-8')
        self.parameters.update({ 'nimi': cgi.escape(self.ruokaaine.nimi),
                                 'ruokaaine_id': self.ruokaaine.ruokaaine_id,
                                 'kuva': kuva_link,
                                 'status': status })

        return [ self.headers, self.parameters ]

    def delete(self):
        if self.authorized(self.ruokaaine_id):
            Ruokaaine.delete(self.ruokaaine_id)

            self.redirect_after_post("%s/ruokaaine?deleted=%d" % (self.conf['script_name'], self.ruokaaine_id))

        self.redirect_after_post("%s/ruokaaine?status=not_authorized" % (self.conf['script_name']))

        return [ self.headers, self.parameters ]
