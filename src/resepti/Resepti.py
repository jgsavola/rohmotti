import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti

class Resepti(DatabaseObject):
    def __init__(self, resepti_id=None, nimi=None, valmistusohje=None, ruokaaineet=None, kommentit=None):
        self.resepti_id = resepti_id
        self.nimi = nimi
        self.valmistusohje = valmistusohje
        self.ruokaaineet = ruokaaineet
        self.kommentit = kommentit

    @classmethod
    def load_from_database(cls, resepti_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT resepti_id, nimi, valmistusohje FROM reseptiohjelma.resepti WHERE resepti_id = %s", (int(resepti_id),))
        row = cur.fetchone()

        resepti = Resepti(row[0], row[1], row[2])

        kommentit = []
        for kommentti_id in Kommentti.load_ids(resepti_id):
            kommentit.append(Kommentti.load_from_database(kommentti_id = kommentti_id))

        resepti.kommentit = kommentit

        return resepti

    @classmethod
    def new(cls, nimi=None, valmistusohje=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.resepti (nimi, valmistusohje) VALUES (%s, %s) RETURNING resepti_id, nimi, valmistusohje", (nimi, valmistusohje))
        cls.conn.commit()

        row = cur.fetchone()

        resepti = Resepti(row[0], row[1])

        return resepti

    @classmethod
    def load_ids(cls):
        cur = cls.conn.cursor()
        cur.execute("SELECT resepti_id FROM reseptiohjelma.resepti")
        for row in cur.fetchall():
            yield row[0]

    def save(self):
        cur = Resepti.conn.cursor()
        cur.execute("UPDATE resepti SET nimi = %s, valmistusohje = %s WHERE resepti_id = %s", (self.nimi, self.valmistusohje, self.resepti_id))
        Resepti.conn.commit()
