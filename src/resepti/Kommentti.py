import psycopg2
from DatabaseObject import DatabaseObject

class Kommentti(DatabaseObject):
    def __init__(self, kommentti_id=None, kohde_id=None, teksti=None, kuva=None, aika=None):
        self.kommentti_id = kommentti_id
        self.kohde_id = kohde_id
        self.teksti = teksti
        self.kuva = kuva
        self.aika = aika

    @classmethod
    def load_from_database(cls, kommentti_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT kommentti_id, kohde_id, teksti, kuva, aika FROM reseptiohjelma.kommentti WHERE kommentti_id = %s", (int(kommentti_id),))
        row = cur.fetchone()

        kommentti = Kommentti(row[0], row[1], row[2], row[3], row[4])

        return kommentti

    @classmethod
    def new(cls, kohde_id=None, teksti=None, kuva=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.kommentti (kohde_id, teksti, kuva) VALUES (%s, %s, %s) RETURNING kommentti_id, kohde_id, teksti, kuva, aika",
                    (kohde_id,
                     teksti,
                     None if kuva is None else psycopg2.Binary(kuva)))
        cls.conn.commit()

        row = cur.fetchone()

        kommentti = Kommentti(*row)

        return kommentti

    @classmethod
    def load_ids(cls, kohde_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT kommentti_id FROM reseptiohjelma.kommentti WHERE kohde_id = %s", (int(kohde_id),))
        for row in cur.fetchall():
            yield row[0]
