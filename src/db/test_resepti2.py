#!/usr/bin/python

import time
import os
import pwd
import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti
from Resepti import Resepti

dbuser = pwd.getpwuid(os.getuid()).pw_name
dbname = dbuser
conn = psycopg2.connect("dbname=%s user=%s" % (dbname, dbuser))

DatabaseObject.setDatabaseConnection(conn)

for id in Resepti.load_ids():
    o = Resepti.load_from_database(id)
    print ": %d -- %s" % (o.resepti_id, o.nimi)

for id in Kommentti.load_ids():
    o = Kommentti.load_from_database(id)
    print ": %d -- %s %s" % (o.kommentti_id, o.aika, o.teksti)

# print "new"
# r = Resepti2.new('testi_' + str(time.time()), 'valmista')

# print "update"
# r.valmistusohje = r.valmistusohje + "_update"
# r.save()

# print "delete"
# Resepti2.delete(r.resepti_id)

print "Korinttikeksit"
k = Resepti.load_from_database(68)
print "    %d %s %s %s" % (k.resepti_id, k.nimi, k.omistaja, k.luotu)

print "Resepti"
print "new"
r = Resepti.new(nimi='testi_' + str(time.time()), valmistusohje='valmista', omistaja=67)
r2 = Resepti.new(nimi='testi2_' + str(time.time()), valmistusohje='valmista', omistaja=67)
print "    %d %s %s %s" % (r.resepti_id, r.nimi, r.omistaja, r.luotu)
print "    %d %s %s %s" % (r2.resepti_id, r2.nimi, r2.omistaja, r2.luotu)

print "update"
r.valmistusohje = r.valmistusohje + "_update"
r.omistaja = 64
r.save()

print "delete"
Resepti.delete(r.resepti_id)

