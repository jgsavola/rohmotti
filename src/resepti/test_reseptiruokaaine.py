#!/usr/bin/python

import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from ReseptiRuokaaine import ReseptiRuokaaine

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

for id in ReseptiRuokaaine.load_ids(resepti_id=10, ruokaaine_id=None):
    o = ReseptiRuokaaine.load_from_database(id[0], id[1])
    print ": %d, %s -- %.0f %s" % (o.resepti.resepti_id, o.ruokaaine.nimi, o.maara, o.mittayksikko)
