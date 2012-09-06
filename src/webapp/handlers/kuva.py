#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import cgi
import cgitb
from basehandler import BaseHandler
from db.Kommentti import Kommentti

class Handler(BaseHandler):
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

        self.kuva_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            self.kuva_id = m.group(1)

    def get(self):
        if self.kuva_id is None:
            return None
        kuva = Kommentti.load_from_database(self.kuva_id)

        #
        # Koska tietokannassa on aikaleima kuvalle, täytetään
        # 'Last-Modified'-otsake. Toivottavasti tämä säästää
        # verkkoliikennettä.
        #
        image_timestamp_utc = kuva.aika - kuva.aika.utcoffset()

        data = str(kuva.kuva)

        print "Content-Type: image/jpeg"
        print "Content-Length: %d" % (len(data))
        print "Last-Modified: %s" % (image_timestamp_utc.strftime('%a, %d %b %Y %H:%M:%S GMT'))
        print ""

        sys.stdout.write(data)

        return None
