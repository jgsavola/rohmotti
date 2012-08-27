#!/usr/bin/python

import os
import pwd
import psycopg2
from Ruokaaine import RuokaaineFactory, Ruokaaine

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

factory = RuokaaineFactory(conn)

suola = factory.load_from_database(4)

print "ruokaaine: %d -- %s" % (suola.ruokaaine_id, suola.nimi)

