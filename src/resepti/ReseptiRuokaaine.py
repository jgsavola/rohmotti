import psycopg2
from DatabaseObject import DatabaseObject
from Resepti import Resepti
from Ruokaaine import Ruokaaine

class ReseptiRuokaaine(DatabaseObject):
    def __init__(self, resepti=None, ruokaaine=None, jarjestys=None, maara=None, mittayksikko=None):
        self.resepti = resepti
        self.ruokaaine = ruokaaine
        self.jarjestys = jarjestys
        self.maara = maara
        self.mittayksikko = mittayksikko

    @classmethod
    def load_from_database(cls, resepti_id, ruokaaine_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT resepti_id, ruokaaine_id, jarjestys, maara, mittayksikko FROM reseptiohjelma.resepti_ruokaaine WHERE resepti_id = %s AND ruokaaine_id = %s", (int(resepti_id), int(ruokaaine_id)))
        row = cur.fetchone()

        resepti   = Resepti.load_from_database(row[0])
        ruokaaine = Ruokaaine.load_from_database(row[1])

        resepti_ruokaaine = ReseptiRuokaaine(resepti, ruokaaine, row[2], row[3], row[4])

        return resepti_ruokaaine

    @classmethod
    def new(cls, resepti=None, ruokaaine=None, jarjestys=None, maara=None, mittayksikko=None):
        cur = cls.conn.cursor()
        cur.execute("INSERT INTO reseptiohjelma.resepti_ruokaaine (resepti_id, ruokaaine_id, jarjestys, maara, mittayksikko) VALUES (%s, %s, %s, %s, %s) RETURNING resepti_id, ruokaaine_id, jarjestys, maara, mittayksikko", (resepti.resepti_id, ruokaaine.ruokaaine_id, jarjestys, maara, mittayksikko))
        cls.conn.commit()

        row = cur.fetchone()

        #
        # FIXME
        #
        resepti_ruokaaine = ReseptiRuokaaine(resepti, ruokaaine, row[2], row[3], row[4])

        return resepti_ruokaaine

    @classmethod
    def load_ids(cls, resepti_id, ruokaaine_id):
        cur = cls.conn.cursor()
        cur.execute("SELECT resepti_id, ruokaaine_id FROM reseptiohjelma.resepti_ruokaaine WHERE resepti_id = %s", (int(resepti_id),))
        for row in cur.fetchall():
            yield (row[0], row[1])
