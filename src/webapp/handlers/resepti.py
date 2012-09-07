#!/usr/bin/python
# -*- coding: utf-8 -*- 

import cgi
from basehandlerwithsession import BaseHandlerWithSession
from db.Resepti import Resepti
from db.ReseptiRuokaaine import ReseptiRuokaaine
from util.html_parser import CommentHTMLParser

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
	<legend>Lisää resepti:</legend>
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
            reseptilista += "<li><a href=\"%s/%d\">%s</a> %s</li>\n" % (self.conf['full_path'], resepti.resepti_id, cgi.escape(resepti.nimi), self.authorized(resepti.resepti_id) and delete_form or '')
        reseptilista += "</ul>\n"

        self.headers.append('Content-Type: text/html; charset=UTF-8')
        self.parameters.update({ 'reseptilista': reseptilista, 
                                 'status': status,
                                 'lisaalomake': lisaalomake
                                 })

        return [ self.headers, self.parameters ]

    def post(self):
        nimi = self.form.getvalue("nimi")

        #
        # Auktorisointi
        #
        if self.sessio is None:
            self.redirect_after_post("%s?status=not_authorized" % (self.conf['full_path'],))
            return [ self.headers, self.parameters ]

        resepti = Resepti.new(nimi=nimi)
        resepti.omistaja = self.sessio.henkilo_id
        resepti.save()

        self.redirect_after_post("%s?inserted=%d" % (self.conf['full_path'], resepti.resepti_id))

        return [ self.headers, self.parameters ]
