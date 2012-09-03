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
        row = None
        try:
            cur = cls.conn.cursor()
            cur.execute("SELECT resepti_id, nimi, valmistusohje FROM reseptiohjelma.resepti WHERE resepti_id = %s", (int(resepti_id),))
            row = cur.fetchone()
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

        resepti = Resepti(*row)

        kommentit = []
        for kommentti_id in Kommentti.load_ids(resepti_id):
            kommentit.append(Kommentti.load_from_database(kommentti_id = kommentti_id))

        resepti.kommentit = kommentit

        return resepti

    @classmethod
    def new(cls, nimi=None, valmistusohje=None):
        row = None
        try:
            cur = cls.conn.cursor()
            cur.execute("INSERT INTO reseptiohjelma.resepti (nimi, valmistusohje) VALUES (%s, %s) RETURNING resepti_id, nimi, valmistusohje", (nimi, valmistusohje))

            row = cur.fetchone()
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

        return Resepti(*row)

    @classmethod
    def load_ids(cls):
        try:
            cur = cls.conn.cursor()
            cur.execute("SELECT resepti_id FROM reseptiohjelma.resepti ORDER BY nimi, resepti_id")
            for row in cur.fetchall():
                yield row[0]
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

    def save(self):
        try:
            cur = Resepti.conn.cursor()
            cur.execute("UPDATE resepti SET nimi = %s, valmistusohje = %s WHERE resepti_id = %s", (self.nimi, self.valmistusohje, self.resepti_id))
        except:
            self.__class__.conn.rollback()
        else:
            self.__class__.conn.commit()

    @classmethod
    def delete(cls, resepti_id):
        try:
            cur = cls.conn.cursor()
            cur.execute("DELETE FROM reseptiohjelma.resepti WHERE resepti_id = %s", (resepti_id,))
        except:
            cls.conn.rollback()
        else:
            cls.conn.commit()
