#!/usr/bin/python

import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from Mittayksikko import Mittayksikko

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

for id in Mittayksikko.load_ids():
    o = Mittayksikko.load_from_database(id)
    print ": %s -- %s, %s, %s" % (o.nimi, o.tyyppi, o.perusyksikko, o.kerroin)
