#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cgi
from db.DatabaseObject import DatabaseObject

class Handler:
    def __init__(self, form, conf):
        self.form = form
        self.conf = conf

    def render(self):
        self.headers = []
        self.headers.append('Content-Type: text/html; charset=UTF-8')

        self.parameters = {}

        henkilo_id = None
        m = re.match(r'.*/(\d+)', self.conf['path_info'])
        if m:
            henkilo_id = m.group(1)

        if self.conf['request_method'] == 'GET':
            q = self.form.getvalue('q')

            query = """SELECT resepti_id, ts_headline('finnish', valmistusohje, to_tsquery('finnish', %s)) FROM resepti WHERE to_tsvector('finnish', valmistusohje) @@ to_tsquery('finnish', %s)"""

            output = []
            try:
                cur = DatabaseObject.conn.cursor()
                cur.execute(query, (q, q))

                row = cur.fetchone()
                while row is not None:
                    html = ("""<a href="%s/resepti/%d">resepti %d</a> %s<br />""" %
                            (self.conf['script_name'],
                             int(row[0]),
                             int(row[0]),
                             row[1]))
                    output.append(html)
                    row = cur.fetchone()
            except:
                DatabaseObject.conn.rollback()
                raise
            else:
                DatabaseObject.conn.commit()

            hakutulos = ''
            if len(output) == 0:
                hakutulos = '<p>Ei osumia</p>'
            else:
                hakutulos = '\n'.join(output)
            self.parameters.update({ 'hakutulos':  hakutulos })

        return [ self.headers, self.parameters ]
