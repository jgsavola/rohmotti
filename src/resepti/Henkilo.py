import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti

class Henkilo(DatabaseObject):
    def __init__(self, henkilo_id=None, nimi=None, tunnus=None, salasana=None, kommentit=None):
        self.henkilo_id = henkilo_id
        self.nimi = nimi
        self.tunnus = tunnus
        self.salasana = salasana
        self.kommentit = kommentit

    @classmethod
    def load_from_database(cls, henkilo_id=None, tunnus=None):
        cur = cls.conn.cursor()

        if henkilo_id is not None:
            cur.execute("SELECT henkilo_id, nimi, tunnus, salasana FROM reseptiohjelma.henkilo WHERE henkilo_id = %s", 
                        (int(henkilo_id),))
        elif tunnus is not None:
            cur.execute("SELECT henkilo_id, nimi, tunnus, salasana FROM reseptiohjelma.henkilo WHERE tunnus = %s",
                        (tunnus,))

        row = cur.fetchone()

        if row is None:
            return None

        henkilo = Henkilo(row[0], row[1], row[2], row[3])

        kommentit = []
        for kommentti_id in Kommentti.load_ids(row[0]):
            kommentit.append(Kommentti.load_from_database(kommentti_id = kommentti_id))

        henkilo.kommentit = kommentit

        return henkilo

    @classmethod
    def new(cls, nimi=None, tunnus=None, salasana=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.henkilo (nimi, tunnus, salasana) VALUES (%s, %s, %s) RETURNING henkilo_id, nimi, tunnus, salasana", (nimi, tunnus, salasana))
        cls.conn.commit()

        row = cur.fetchone()

        henkilo = Henkilo(row[0], row[1], row[2], row[3])

        return henkilo

    @classmethod
    def load_ids(cls):
        cur = cls.conn.cursor()
        cur.execute("SELECT henkilo_id FROM reseptiohjelma.henkilo")
        for row in cur.fetchall():
            yield row[0]
