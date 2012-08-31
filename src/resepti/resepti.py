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

        headers = []
        headers.append('Content-Type: text/html; charset=UTF-8')

        parameters = {}

        resepti_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            resepti_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            if resepti_id is not None:
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

                parameters = { 'nimi': resepti.nimi,
                               'resepti_id': resepti.resepti_id,
                               'valmistusohje': valmistusohje_text,
                               'kuva': kuva_link,
                               'ruokaaineetlista': ruokaaineetlista,
                               'status': '' }
            else:
                reseptilista = "<ul class=\"ruokaainelista\">\n"
                for id in Resepti.load_ids():
                    resepti = Resepti.load_from_database(id)
                    reseptilista += "<li><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], resepti.resepti_id, cgi.escape(resepti.nimi))
                reseptilista += "</ul>\n"
                parameters = {'reseptilista': reseptilista, 'status': ''}
        elif os.environ['REQUEST_METHOD'] == 'POST':
            if resepti_id is None:
                nimi = self.form.getvalue("nimi")

                resepti = Resepti.new(nimi=nimi)

                reseptilista = "<ul>\n"
                for id in Resepti.load_ids():
                    resepti = Resepti.load_from_database(id)
                    reseptilista += "<li><a href=\"%s/%d\">%d</a> %s</li>\n" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id, resepti.nimi)
                reseptilista += "</ul>\n"

                s = "<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" % (self.conf['request_uri'], resepti.resepti_id, resepti.resepti_id)
                parameters = {'reseptilista': reseptilista, 'status': s}
            else:
                valmistusohje_unsafe = self.form.getvalue('valmistusohje')

                #
                # Run the HTML input through the parser which allows only
                # a safe subset of HTML.
                #
                parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                parser.feed(valmistusohje_unsafe)
                valmistusohje = parser.output

                resepti = Resepti.load_from_database(resepti_id = resepti_id)

                resepti.valmistusohje = valmistusohje
                resepti.save()

                kuva_link = ''
                for kommentti in resepti.kommentit:
                    kuva_link += "<img src=\"%s/../../kuva/%d\"/>\n" % (self.conf['request_uri'], kommentti.kommentti_id)

                ruokaaineetlista = self.create_ruokaaineet_list(resepti_id)

                valmistusohje_text = resepti.valmistusohje
                mode = self.form.getvalue('mode')
                if mode == 'edit':
                    valmistusohje_text = textwrap.dedent("""\
                        <form action="%s%s" method="post">
                            <textarea name="valmistusohje" rows="10" cols="60">%s</textarea>
                            <input type="submit" value="submit" />
                        </form>""" % (self.conf['script_name'], self.conf['path_info'], valmistusohje_text))

                parameters = { 'nimi': resepti.nimi,
                               'resepti_id': resepti.resepti_id,
                               'valmistusohje': valmistusohje_text,
                               'kuva': kuva_link,
                               'ruokaaineetlista': ruokaaineetlista,
                               'status': '<p class="status">Tallennettu.</p>'}

        return [ headers, parameters ]

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
