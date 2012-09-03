#!/usr/bin/python

import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from Resepti import Resepti

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

for id in Resepti.load_ids():
    o = Resepti.load_from_database(id)
    print ": %d -- %s" % (o.resepti_id, o.nimi)

