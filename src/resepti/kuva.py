#!/usr/bin/python

import sys
import os
import re
import psycopg2
import json
import cgi
import cgitb
from Kommentti import Kommentti, KommenttiFactory

class Handler:
    def __init__(self, conn, form, conf):
        self.conn = conn
        self.form = form
        self.conf = conf
        self.kommenttiFactory = KommenttiFactory(conn)

    def render(self):
        path_info = self.conf['path_info']

        kuva_id = None
        m = re.match(r'.*/(\d+)', path_info)
        if m:
            kuva_id = m.group(1)

        if os.environ['REQUEST_METHOD'] == 'GET':
            if kuva_id is not None:
                print "Content-Type: image/jpeg\n"

                kuva = self.kommenttiFactory.load_from_database(kommentti_id = kuva_id)

                sys.stdout.write(str(kuva.kuva))

                return None
            else:
                return None
        elif os.environ['REQUEST_METHOD'] == 'POST':
            return None
