#!/usr/bin/python

import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

kuva = Kommentti.load_from_database(3)

print "kommentti: %d -- %s" % (kuva.kommentti_id, kuva.teksti)

ids = Kommentti.load_ids(kohde_id=10)
for i in ids:
    print "  kommentti(kohde_id=10): %d" % (i)
