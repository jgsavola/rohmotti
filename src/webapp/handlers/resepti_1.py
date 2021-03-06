#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
import textwrap
from basehandlerwithsession import BaseHandlerWithSession
from db.Resepti import Resepti
from db.ReseptiRuokaaine import ReseptiRuokaaine
from db.Ruokaaine import Ruokaaine
from db.Mittayksikko import Mittayksikko
from db.Kommentti import Kommentti
from db.Henkilo import Henkilo
from util.html_parser import CommentHTMLParser

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

        self.resepti_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.resepti_id = int(m.group(1))

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

    def get(self):
        edit = self.form.getvalue('edit')

        self.resepti = Resepti.load_from_database(self.resepti_id)

        self.render_kohdeinfo(self.resepti)

        kuva_link = ''
        for kommentti in self.resepti.kommentit:
            tunnus = '<span class="tuntematon">tuntematon</span>'
            if kommentti.omistaja is not None:
                omistaja = Henkilo.load_from_database(kommentti.omistaja)
                tunnus = omistaja.tunnus

            delete_form = ''
            if self.authorized():
                delete_form = """<form class="deleteform" action="%s/kommentti/%d" method="post">
                                   <input type="hidden" name="method_override" value="DELETE" />
                                   <input type="submit" value="Poista" class="deleteform" />
                                 </form>""" % (self.conf['full_path'], kommentti.kommentti_id)

            kuva_link += "<div class=\"comment\">"
            kuva_link += "<div class=\"timestamp\">%s %s %s</div>\n" % (tunnus, kommentti.aika, delete_form)
            if kommentti.kuva is not None:
                kuva_link += "<img src=\"%s/kuva/%d\" alt=\"%s\" />\n" % (
                    self.conf['script_name'],
                    kommentti.kommentti_id,
                    '')
            kuva_link += "<div class=\"commenttext\">%s</div>\n" % (kommentti.teksti)
            kuva_link += "</div>"

        ruokaaineetlista = self.create_ruokaaineet_list(self.resepti.resepti_id)

        valmistusohje_text = "<div class=\"valmistusohje\">%s</div>" % (self.resepti.valmistusohje)
        if self.authorized():
            if edit is not None:
                valmistusohje_text = textwrap.dedent("""\
                    <form class="cmxform" action="%s%s" method="post">
                      <fieldset>
                        <legend></legend>
                        <ol>
                          <li>
                            <textarea name="valmistusohje" rows="10" cols="60" id="valmistusohje">%s</textarea>
                          </li>
                          <li>
                            <input type="submit" value="Tallenna" />
                          </li>
                          <input type="hidden" name="action" value="updaterecipe"</input>
                        </ol>
                      </fieldset>
                    </form>""" % (self.conf['script_name'], self.conf['path_info'], self.resepti.valmistusohje))
            else:
                valmistusohje_text = valmistusohje_text + """\
                    <form action="%s">
                      <input type="submit" name="edit" value="Muokkaa" />
                    </form>""" % (self.conf['full_path'])

        lisaalomake = ''
        if self.authorized():
            ruokaaine_optiot = self.create_ruokaaine_optiot()
            mittayksikko_optiot = self.create_mittayksikko_optiot()

            lisaalomake = """\
          <form class="cmxform" action="%s/ruokaaine" method="post" enctype="multipart/form-data">
            <fieldset>
              <legend>Lisää ruoka-aine:</legend>
              <ol>
                <li>
                  <label for="ruokaaine_id">Ruoka-aine</label>
                  <select name="ruokaaine_id" id="ruokaaine_id">
                    %s
                  </select>
                </li>
                <li>
                  <label for="maara">Määrä</label>
                  <input type="text" name="maara" id="maara" />
                </li>
                <li>
                  <label for="mittayksikko">Mittayksikko</label>
                  <select name="mittayksikko" id="mittayksikko">
                    %s
                  </select>
                </li>
                <li>
                  <input type="submit" value="Lisää" />
                </li>
                <input type="hidden" name="action" value="add" />
              </ol>
            </fieldset>
          </form>
            """ % (self.conf['full_path'], ruokaaine_optiot, mittayksikko_optiot)


        status = ''
        if self.form.getvalue('updated', '') == 'true':
            status = '<p class="status">Tallennettu.</p>'
        elif self.form.getvalue('comment_created') is not None:
            status = '<p class="status">Uusi kommentti: %d</p>' % (int(self.form.getvalue('comment_created')))

        self.headers.append('Content-Type: text/html; charset=UTF-8')
        self.parameters.update({ 'nimi': self.resepti.nimi,
                                 'resepti_id': self.resepti.resepti_id,
                                 'valmistusohje': valmistusohje_text,
                                 'kuva': kuva_link,
                                 'ruokaaineetlista': ruokaaineetlista,
                                 'status': status,
                                 'lisaalomake': lisaalomake
                                 })

        return [ self.headers, self.parameters ]


    def render_kohdeinfo(self, resepti):
        luotu = resepti.luotu.strftime("%d.%m.%y %H:%M")
        tunnus = '<span class="tuntematon">tuntematon</span>'
        if resepti.omistaja is not None:
            omistaja = Henkilo.load_from_database(resepti.omistaja)
            tunnus = omistaja.tunnus

        kohdeinfo = """%s<br />%s""" % (tunnus, luotu)

        self.parameters.update({ 'kohdeinfo': kohdeinfo })

    def create_ruokaaine_optiot(self):
        options = ''
        for ruokaaine_id in Ruokaaine.load_ids():
            ruokaaine = Ruokaaine.load_from_database(ruokaaine_id)
            options = options + ("<option value=\"%d\">%s</option>\n" %
                                 (ruokaaine_id, ruokaaine.nimi))

        return options

    def create_mittayksikko_optiot(self):
        options = ''
        for nimi in Mittayksikko.load_ids():
            options = options + ("<option value=\"%s\">%s</option>\n" %
                                 (nimi, nimi))

        return options

    def post(self):
        if self.authorized(self.resepti_id):
            action = self.form.getvalue('action')

            if action == 'updaterecipe':
                valmistusohje_unsafe = self.form.getvalue('valmistusohje')

                #
                # Salli vain turvallisten HTML-tagien käyttö kommenteissa.
                #
                parser = CommentHTMLParser(ok_tags=['p', 'strong', 'pre', 'em', 'b', 'br', 'i', 'hr', 's', 'sub', 'sup', 'tt', 'u'])
                valmistusohje = parser.parse_string(valmistusohje_unsafe)

                self.resepti = Resepti.load_from_database(self.resepti_id)

                self.resepti.valmistusohje = valmistusohje
                self.resepti.save()

                self.redirect_after_post("%s?updated=true" % (self.conf['full_path']))
        else:
            self.redirect_after_post("%s/resepti?status=not_authorized" % (self.conf['script_name']))

        return [ self.headers, self.parameters ]

    def delete(self):
        if self.authorized(self.resepti_id):
            Resepti.delete(self.resepti_id)

            self.redirect_after_post("%s/resepti?deleted=%d" % (self.conf['script_name'], self.resepti_id))
        else:
            self.redirect_after_post("%s/resepti?status=not_authorized" % (self.conf['script_name']))

        return [ self.headers, self.parameters ]
