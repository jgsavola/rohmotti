#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti
from SimpleDatabaseObject import SimpleDatabaseObject

class Kohde(SimpleDatabaseObject):
    @classmethod
    def delete(cls, _id, **kwargs):
        delete_sql = 'DELETE FROM reseptiohjelma.kohde WHERE kohde_id = %s'

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()

            super(Kohde, cls).delete(_id, _cursor=my_cursor)

            my_cursor.execute(delete_sql, (_id,))
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

class Resepti3(Kohde):
    id_column = 'resepti_id'
    other_columns = ['nimi', 'valmistusohje']
    table_name = 'reseptiohjelma.resepti'

class Kommentti(SimpleDatabaseObject):
    id_column = 'kommentti_id'
    other_columns = ['teksti', 'kuva', 'aika']
    table_name = 'reseptiohjelma.kommentti'

