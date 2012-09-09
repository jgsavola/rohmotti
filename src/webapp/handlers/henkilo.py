#!/usr/bin/python
# -*- coding: utf-8 -*- 

import re
import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Henkilo import Henkilo
from db.Rajoitus import Rajoitus
from db.Ruokaaine import Ruokaaine

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

        self.henkilo_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.henkilo_id = m.group(1)

    def get(self):
        if self.henkilo_id is not None:
            henkilo = Henkilo.load_from_database(self.henkilo_id)

            #
            # Älä näytä rajoituksia kirjautumattomille käyttäjille
            # yksilönsuojasyistä.
            #
            self.render_restriction_list()

            lisaalomake = ''
            if self.authorized():

                lisaalomake = """\
        <form class="cmxform" action="%s/rajoitus" method="post">
          <fieldset>
            <legend>Lisää rajoitus:</legend>
            <ol>
  	      <li>
	        <label for="ruokaaine_id">Ruoka-aine</label>
  	        <select name="ruokaaine_id" id="ruokaaine_id" autofocus>
		  %s
  	        </select>
  	      </li>
              <li>
                <label for="rajoitus">Rajoitus</label>
                <input type="text" name="rajoitus"/>
              </li>
              <li>
                <input type="submit" value="Lisää" />
              </li>
            </ol>
          </fieldset>
        </form>
    """ % (self.conf['full_path'], self.create_ruokaaine_optiot())

            self.parameters.update({ 'lisaalomake': lisaalomake })

            kuva_link = ''
            for kommentti in henkilo.kommentit:
                kuva_link += "<img src=\"%s/../../kuva/%d\" alt=\"%s\" />\n" % (
                    self.conf['request_uri'],
                    kommentti.kommentti_id,
                    cgi.escape(kommentti.teksti))

            self.parameters.update({ 'nimi': henkilo.nimi,
                                     'henkilo_id': henkilo.henkilo_id,
                                     'tunnus': henkilo.tunnus,
                                     'kuva': kuva_link,
                                     })
        else:
            henkilolista = self.render_henkilolista()

            self.parameters.update({ 'henkilolista': henkilolista, 'status': '' })

        self.headers.append('Content-Type: text/html; charset=UTF-8')

        return [ self.headers, self.parameters ]

    def post(self):
        nimi = self.form.getvalue("nimi")

        henkilo = Henkilo.new(nimi=nimi)

        henkilolista = self.render_henkilolista()

        self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], henkilo.henkilo_id))
        return [ self.headers, self.parameters ]

    def render_henkilolista(self):
        henkilolista = "<ul class=\"henkilolista\">\n"
        for id in Henkilo.load_ids():
            henkilo = Henkilo.load_from_database(id)
            henkilolista += "<li class=\"henkilolista\"><a href=\"%s/%d\">%s</a></li>\n" % (self.conf['request_uri'], henkilo.henkilo_id, cgi.escape(henkilo.nimi))
        henkilolista += "</ul>\n"

        return henkilolista

    def render_restriction_list(self):
        if not self.authorized():
            rajoituslista = 'Kirjaudu, jos haluat nähdä rajoitukset.'
        else:
            rajoituksia = 0
            rajoituslista = '<ul class="rajoituslista">'
            for rajoitus_id in Rajoitus.load_ids(henkilo_id=self.henkilo_id):
                rajoituksia = rajoituksia + 1
                rajoitus = Rajoitus.load_from_database(rajoitus_id)
                ruokaaine = Ruokaaine.load_from_database(rajoitus.ruokaaine_id)

                ruokaaine_link = ("""<a href="%s/ruokaaine/%d">%s</a>""" %
                                  (self.conf['script_name'],
                                   rajoitus.ruokaaine_id,
                                   ruokaaine.nimi))

                rajoituslista += '<li>%s: %s</li>' % (rajoitus.rajoitus, ruokaaine_link)
            rajoituslista += "</ul>"

            if rajoituksia == 0:
                rajoituslista = 'Ei rajoituksia.'

        self.parameters.update({ 'rajoituslista': rajoituslista })

    def create_ruokaaine_optiot(self):
        options = ''
        for ruokaaine_id in Ruokaaine.load_ids():
            ruokaaine = Ruokaaine.load_from_database(ruokaaine_id)
            options = options + ("<option value=\"%d\">%s</option>\n" %
                                 (ruokaaine_id, ruokaaine.nimi))

        return options
