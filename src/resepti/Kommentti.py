import psycopg2

class Kommentti:
    def __init__(self, kommentti_id=None, kohde_id=None, teksti=None, kuva=None, aika=None):
        self.kommentti_id = kommentti_id
        self.kohde_id = kohde_id
        self.teksti = teksti
        self.kuva = kuva
        self.aika = aika

class KommenttiFactory:
    def __init__(self, conn):
        self.conn = conn

    def load_from_database(self, kommentti_id):
        cur = self.conn.cursor()
        cur.execute("SELECT kommentti_id, kohde_id, teksti, kuva, aika FROM reseptiohjelma.kommentti WHERE kommentti_id = %s", (int(kommentti_id),))
        row = cur.fetchone()

        kommentti = Kommentti(row[0], row[1], row[2], row[3], row[4])

        return kommentti

    def new(self, nimi=None):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.kommentti (nimi) VALUES (%s) RETURNING kommentti_id, nimi", (nimi,))
        self.conn.commit()

        row = cur.fetchone()

        kommentti = Kommentti(row[0], row[1])

        return kommentti

    def load_ids(self, kohde_id):
        cur = self.conn.cursor()
        cur.execute("SELECT kommentti_id FROM reseptiohjelma.kommentti WHERE kohde_id = %s", (int(kohde_id),))
        for row in cur.fetchall():
            yield row[0]
