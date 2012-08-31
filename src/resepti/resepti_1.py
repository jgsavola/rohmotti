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
from html_parser import CommentHTMLParser

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        path_info = os.environ.get('PATH_INFO', '')

        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        resepti_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            resepti_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            resepti = Resepti.load_from_database(resepti_id = resepti_id)

            kuva_link = ''
            for kommentti in resepti.kommentit:
                kuva_link += "<img src=\"%s/../../kuva/%d\" />\n" % (self.conf['request_uri'], kommentti.kommentti_id)

            ruokaaineetlista = self.create_ruokaaineet_list(resepti_id)

            valmistusohje_text = resepti.valmistusohje
            mode = self.form.getvalue('mode')
            if mode == 'edit':
                valmistusohje_text = textwrap.dedent("""\
                    <form action="%s%s" method="post">
                        <textarea name="valmistusohje" rows="10" cols="60">%s</textarea>
                        <input type="submit" value="submit" />
                    </form>""" % (self.conf['script_name'], self.conf['path_info'], valmistusohje_text))

            self.parameters.update({ 'nimi': resepti.nimi,
                                     'resepti_id': resepti.resepti_id,
                                     'valmistusohje': valmistusohje_text,
                                     'kuva': kuva_link,
                                     'ruokaaineetlista': ruokaaineetlista,
                                     'status': '' })
        elif os.environ['REQUEST_METHOD'] == 'POST':
            valmistusohje_unsafe = self.form.getvalue('valmistusohje')

            #
            # Salli vain turvallisten HTML-tagien käyttö kommenteissa.
            #
            parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
            valmistusohje = parser.parse_string(valmistusohje_unsafe)

            resepti = Resepti.load_from_database(resepti_id = resepti_id)

            resepti.valmistusohje = valmistusohje
            resepti.save()

            kuva_link = ''
            for kommentti in resepti.kommentit:
                kuva_link += "<img src=\"%s/../../kuva/%d\" />\n" % (self.conf['request_uri'], kommentti.kommentti_id)

            ruokaaineetlista = self.create_ruokaaineet_list(resepti_id)

            valmistusohje_text = resepti.valmistusohje
            mode = self.form.getvalue('mode')
            if mode == 'edit':
                valmistusohje_text = textwrap.dedent("""\
                    <form action="%s%s" method="post">
                        <textarea name="valmistusohje" rows="10" cols="60">%s</textarea>
                        <input type="submit" value="submit" />
                    </form>""" % (self.conf['script_name'], self.conf['path_info'], valmistusohje_text))

            self.parameters.update({ 'nimi': resepti.nimi,
                                     'resepti_id': resepti.resepti_id,
                                     'valmistusohje': valmistusohje_text,
                                     'kuva': kuva_link,
                                     'ruokaaineetlista': ruokaaineetlista,
                                     'status': '<p class="status">Tallennettu.</p>' })

        return [ self.headers, self.parameters ]

    def create_ruokaaineet_list(self, resepti_id):
        items = []

        items.append('<ul>')

        for reseptiruokaaine_id in ReseptiRuokaaine.load_ids(resepti_id = resepti_id, ruokaaine_id = None):
            reseptiruokaaine = ReseptiRuokaaine.load_from_database(reseptiruokaaine_id[0], reseptiruokaaine_id[1])
            ruokaaine_link = ("<a href=\"%s%s/../../ruokaaine/%d\">%s</a>" %
                              (self.conf['script_name'],
                               self.conf['path_info'],
                               reseptiruokaaine.ruokaaine.ruokaaine_id,
                               cgi.escape(reseptiruokaaine.ruokaaine.nimi)))

            items.append("<li>%s %d %s</li>\n" %
                         (ruokaaine_link,
                          reseptiruokaaine.maara,
                          cgi.escape(reseptiruokaaine.mittayksikko)))

        items.append('</ul>')

        return '\n'.join(items)
