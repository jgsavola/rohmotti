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

            hakutulos = ''
            if q is not None:
                hakutulos = self.do_query(q)
            self.parameters.update({ 'hakutulos':  hakutulos, 'query': q or '' })

        return [ self.headers, self.parameters ]

    def do_query(self, q):
        query = """WITH query AS ( SELECT to_tsquery('finnish', %s) tsq ) SELECT nimi, resepti_id, ts_headline('finnish', muodosta_reseptin_teksti(resepti_id), query.tsq) FROM resepti, query WHERE resepti.tsv @@ query.tsq"""

        output = []
        try:
            cur = DatabaseObject.conn.cursor()
            cur.execute(query, (q,))

            row = cur.fetchone()
            while row is not None:
                nimi = row[0]
                resepti_id = row[1]
                headline = row[2]

                uri = """%s/resepti/%d""" % (self.conf['script_name'], resepti_id)
                html = ("""<p class="hakutulos"><a href="%s">%s</a> (%s)<br />%s</p>""" %
                        (uri, nimi, uri, headline))
                output.append(html)
                row = cur.fetchone()
        except:
            DatabaseObject.conn.rollback()
            raise
        else:
            DatabaseObject.conn.commit()

        if len(output):
            return '\n'.join(output)
        else:
            return '<p>Ei osumia</p>'
