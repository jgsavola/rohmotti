import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti

class Ruokaaine(DatabaseObject):
    def __init__(self, ruokaaine_id=None, nimi=None, kommentit=None):
        self.ruokaaine_id = ruokaaine_id
        self.nimi = nimi
        self.kommentit = kommentit

    @classmethod
    def load_from_database(cls, ruokaaine_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT ruokaaine_id, nimi FROM reseptiohjelma.ruokaaine WHERE ruokaaine_id = %s", (int(ruokaaine_id),))
        row = cur.fetchone()

        ruokaaine = Ruokaaine(row[0], row[1])

        kommentit = []
        for kommentti_id in Kommentti.load_ids(ruokaaine_id):
            kommentit.append(Kommentti.load_from_database(kommentti_id = kommentti_id))

        ruokaaine.kommentit = kommentit

        return ruokaaine

    @classmethod
    def new(cls, nimi=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.ruokaaine (nimi) VALUES (%s) RETURNING ruokaaine_id, nimi", (nimi,))
        cls.conn.commit()

        row = cur.fetchone()

        ruokaaine = Ruokaaine(row[0], row[1])

        return ruokaaine

    @classmethod
    def load_ids(cls):
        cur = cls.conn.cursor()
        cur.execute("SELECT ruokaaine_id FROM reseptiohjelma.ruokaaine ORDER BY nimi, ruokaaine_id")
        for row in cur.fetchall():
            yield row[0]

    @classmethod
    def delete(cls, ruokaaine_id):
        cur = cls.conn.cursor()
        cur.execute("DELETE FROM reseptiohjelma.ruokaaine WHERE ruokaaine_id = %s", (ruokaaine_id,))
        cls.conn.commit()
