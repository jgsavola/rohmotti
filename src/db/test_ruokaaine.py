#!/usr/bin/python

import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from Ruokaaine import Ruokaaine

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

suola = Ruokaaine.load_from_database(4)

print "ruokaaine: %d -- %s" % (suola.ruokaaine_id, suola.nimi)

