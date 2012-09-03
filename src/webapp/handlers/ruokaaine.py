#!/usr/bin/python
# -*- coding: utf-8 -*- 

import cgi
from db.Ruokaaine import Ruokaaine

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
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
        status = ''

        ruokaaine_id_input = self.form.getvalue('inserted')
        if ruokaaine_id_input is not None:
            ruokaaine_id = int(ruokaaine_id_input)
            status = ("<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['full_path'], ruokaaine_id, ruokaaine_id))

        ruokaaine_id_input = self.form.getvalue('deleted')
        if ruokaaine_id_input is not None:
            ruokaaine_id = int(ruokaaine_id_input)
            status = ("<p class=\"status\">Poistettu: <a href=\"%s/%d\">%d</a></p>" %
                      (self.conf['full_path'], ruokaaine_id, ruokaaine_id))

        ruokaainelista = "<ul class=\"ruokaainelista\">\n"
        for id in Ruokaaine.load_ids():
            ruokaaine = Ruokaaine.load_from_database(id)
            delete_form = """<form class="deleteform" action="%s/%d" method="post">
                               <input type="hidden" name="method_override" value="DELETE" />
                               <input type="submit" value="Poista" class="deleteform" />
                             </form>""" % (self.conf['full_path'], ruokaaine.ruokaaine_id)
            ruokaainelista += ("""<li class="ruokaainelista">
                                  <a href="%s/%d">%s</a> %s</li> """ %
                               (self.conf['request_uri'],
                                ruokaaine.ruokaaine_id,
                                cgi.escape(ruokaaine.nimi),
                                delete_form))
        ruokaainelista += "</ul>\n"

        self.parameters.update({'ruokaainelista': ruokaainelista, 'status': status})
