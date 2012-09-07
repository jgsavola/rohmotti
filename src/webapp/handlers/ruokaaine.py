#!/usr/bin/python
# -*- coding: utf-8 -*- 

import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Ruokaaine import Ruokaaine

class Handler(BaseHandlerWithSession):
    def __init__(self, form, conf):
        super(Handler, self).__init__(form, conf)

    def get(self):
        status = ''

        lisaalomake = ''
        if self.authorized():
            lisaalomake = """\
    <form class="cmxform" action="%s" method="post">
      <fieldset>
	<legend>Lisää ruokaaine:</legend>
	<ol>
	  <li>
	    <input type="text" name="nimi" autofocus />
	  </li>
	  <li>
	    <input type="submit" value="Lisää!" />
	  </li>
	</ol>
      </fieldset>
    </form>
""" % (self.conf['full_path'])

        request_status = self.form.getvalue('status')
        if request_status is not None and request_status == 'not_authorized':
            status = "<p class=\"status\">Toiminto kielletty.</p>"

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
                                    <a href="%s/%d">%s</a> %s
                                  </li>""" %
                               (self.conf['full_path'],
                                ruokaaine.ruokaaine_id,
                                cgi.escape(ruokaaine.nimi),
                                self.authorized(ruokaaine.ruokaaine_id) and delete_form or ''))
        ruokaainelista += "</ul>\n"

        self.headers.append('Content-Type: text/html; charset=UTF-8')
        self.parameters.update({ 'ruokaainelista': ruokaainelista,
                                 'status': status,
                                 'lisaalomake': lisaalomake
                                 })

        return [ self.headers, self.parameters ]

    def post(self):
        nimi = self.form.getvalue("nimi")

        ruokaaine = Ruokaaine.new(nimi=nimi)
        status = ("<p class=\"status\">Lisätty: <a href=\"%s/%d\">%d</a></p>" %
                  (self.conf['request_uri'],
                   ruokaaine.ruokaaine_id,
                   ruokaaine.ruokaaine_id))

        self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], ruokaaine.ruokaaine_id))

        return [ self.headers, self.parameters ]
