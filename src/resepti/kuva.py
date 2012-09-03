#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import cgi
import cgitb
from Kommentti import Kommentti

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        kuva_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            kuva_id = m.group(1)

        if self.conf['request_method'] == 'GET':
            if kuva_id is not None:
                kuva = Kommentti.load_from_database(kommentti_id = kuva_id)

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
            else:
                return None
        elif self.conf['request_method'] == 'POST':
            return None
