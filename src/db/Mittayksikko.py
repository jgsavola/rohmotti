import psycopg2
from DatabaseObject import DatabaseObject

class Mittayksikko(DatabaseObject):
    def __init__(self, nimi=None, tyyppi=None, perusyksikko=None, kerroin=None):
        self.nimi = nimi
        self.tyyppi = tyyppi
        self.perusyksikko = perusyksikko
        self.kerroin = kerroin

    @classmethod
    def load_from_database(cls, nimi):
        cur = cls.conn.cursor()
        cur.execute("SELECT nimi, tyyppi, perusyksikko, kerroin FROM reseptiohjelma.mittayksikko WHERE nimi = %s", (nimi,))
        row = cur.fetchone()

        mittayksikko = Mittayksikko(*row)

        return mittayksikko

    @classmethod
    def new(cls, nimi=None, tyyppi=None, perusyksikko=None, kerroin=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.mittayksikko (nimi, tyyppi, perusyksikko, kerroin) VALUES (%s, %s, %s, %s) RETURNING nimi, tyyppi, perusyksikko, kerroin",
                    (nimi,
                     tyyppi,
                     perusyksikko,
                     kerroin))
        cls.conn.commit()

        row = cur.fetchone()

        mittayksikko = Mittayksikko(*row)

        return mittayksikko

    @classmethod
    def load_ids(cls):
        cur = cls.conn.cursor()
        cur.execute("SELECT nimi FROM reseptiohjelma.mittayksikko ORDER BY nimi")
        for row in cur.fetchall():
            yield row[0]

    @classmethod
    def delete(cls, nimi):
        cur = cls.conn.cursor()
        cur.execute("DELETE FROM reseptiohjelma.mittayksikko WHERE nimi = %s", (nimi,))
        cls.conn.commit()
