import psycopg2
from Kommentti import KommenttiFactory

class Ruokaaine:
    def __init__(self, ruokaaine_id=None, nimi=None, kommentit=None):
        self.ruokaaine_id = ruokaaine_id
        self.nimi = nimi
        self.kommentit = kommentit

class RuokaaineFactory:
    def __init__(self, conn):
        self.conn = conn

    def load_from_database(self, ruokaaine_id):
        cur = self.conn.cursor()
        cur.execute("SELECT ruokaaine_id, nimi FROM reseptiohjelma.ruokaaine WHERE ruokaaine_id = %s", (int(ruokaaine_id),))
        row = cur.fetchone()

        ruokaaine = Ruokaaine(row[0], row[1])

        kommenttiFactory = KommenttiFactory(self.conn)
        kommentit = []
        for kommentti_id in kommenttiFactory.load_ids(ruokaaine_id):
            kommentit.append(kommenttiFactory.load_from_database(kommentti_id = kommentti_id))

        ruokaaine.kommentit = kommentit

        return ruokaaine

    def new(self, nimi=None):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.ruokaaine (nimi) VALUES (%s) RETURNING ruokaaine_id, nimi", (nimi,))
        self.conn.commit()

        row = cur.fetchone()

        ruokaaine = Ruokaaine(row[0], row[1])

        return ruokaaine

    def load_ids(self):
        cur = self.conn.cursor()
        cur.execute("SELECT ruokaaine_id FROM reseptiohjelma.ruokaaine")
        for row in cur.fetchall():
            yield row[0]
