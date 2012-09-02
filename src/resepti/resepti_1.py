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
from Kommentti import Kommentti
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.mode = self.form.getvalue('mode')

        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        self.resepti_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.resepti_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            self.resepti = Resepti.load_from_database(resepti_id = self.resepti_id)

            self.render_page()
        elif os.environ['REQUEST_METHOD'] == 'POST':
            action = self.form.getvalue('action')

            if action == 'updaterecipe':
                valmistusohje_unsafe = self.form.getvalue('valmistusohje')

                #
                # Salli vain turvallisten HTML-tagien käyttö kommenteissa.
                #
                parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                valmistusohje = parser.parse_string(valmistusohje_unsafe)

                self.resepti = Resepti.load_from_database(resepti_id = self.resepti_id)

                self.resepti.valmistusohje = valmistusohje
                self.resepti.save()

                self.redirect_after_post("%s?updated=true" % (self.conf['full_path']))
            elif action == 'upload':
                teksti_input = self.form.getvalue('teksti')
                teksti = None

                if teksti_input is not None:
                    parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                    teksti = parser.parse_string(teksti_input)

                kuva_input = self.form.getvalue('kuva')

                kommentti = Kommentti.new(self.resepti_id, teksti, kuva_input)
                self.resepti = Resepti.load_from_database(resepti_id = self.resepti_id)

                self.redirect_after_post("%s?comment_created=%d" % (self.conf['full_path'], kommentti.kommentti_id))
            self.render_page()

        return [ self.headers, self.parameters ]

    def create_ruokaaineet_list(self, resepti_id):
        items = []

        items.append('<ul>')

        for reseptiruokaaine_id in ReseptiRuokaaine.load_ids(resepti_id = resepti_id, ruokaaine_id = None):
            reseptiruokaaine = ReseptiRuokaaine.load_from_database(reseptiruokaaine_id[0], reseptiruokaaine_id[1])
            ruokaaine_link = ("<a href=\"%s/ruokaaine/%d\">%s</a>" %
                              (self.conf['script_name'],
                               reseptiruokaaine.ruokaaine.ruokaaine_id,
                               cgi.escape(reseptiruokaaine.ruokaaine.nimi)))

            items.append("<li>%s %d %s</li>\n" %
                         (ruokaaine_link,
                          reseptiruokaaine.maara,
                          cgi.escape(reseptiruokaaine.mittayksikko)))

        items.append('</ul>')

        return '\n'.join(items)

    def render_page(self):
        kuva_link = ''
        for kommentti in self.resepti.kommentit:
            kuva_link += "<div class=\"comment\">"
            kuva_link += "<div class=\"timestamp\">%s</div>\n" % (kommentti.aika)
            kuva_link += "<img src=\"%s/kuva/%d\" alt=\"%s\" />\n" % (
                self.conf['script_name'],
                kommentti.kommentti_id,
                '')
            kuva_link += "<div class=\"commenttext\">%s</div>\n" % (kommentti.teksti)
            kuva_link += "</div>"

        ruokaaineetlista = self.create_ruokaaineet_list(self.resepti.resepti_id)

        valmistusohje_text = "<div class=\"valmistusohje\">%s</div>" % (self.resepti.valmistusohje)
        if self.mode == 'edit':
            valmistusohje_text = textwrap.dedent("""\
                <form class="cmxform" action="%s%s" method="post">
                  <fieldset>
                    <legend></legend>
                    <ol>
                      <li>
                        <textarea name="valmistusohje" rows="10" cols="60" id="valmistusohje">%s</textarea>
                      </li>
                      <li>
                        <input type="submit" value="submit" />
                      </li>
                      <input type="hidden" name="action" value="updaterecipe"</input>
                    </ol>
                  </fieldset>
                </form>""" % (self.conf['script_name'], self.conf['path_info'], self.resepti.valmistusohje))


        status = ''
        if self.form.getvalue('updated', '') == 'true':
            status = '<p class="status">Tallennettu.</p>'
        elif self.form.getvalue('comment_created') is not None:
            status = '<p class="status">Uusi kommentti: %d</p>' % (int(self.form.getvalue('comment_created')))

        self.parameters.update({ 'nimi': self.resepti.nimi,
                                 'resepti_id': self.resepti.resepti_id,
                                 'valmistusohje': valmistusohje_text,
                                 'kuva': kuva_link,
                                 'ruokaaineetlista': ruokaaineetlista,
                                 'status': status })

    def redirect_after_post(self, location):
        self.headers.append('Status: 303 See Other')
        self.headers.append("Location: %s" % (location))
