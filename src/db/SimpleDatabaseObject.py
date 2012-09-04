#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from DatabaseObject import DatabaseObject

#
# Transaktioiden hallinnasta:
#
# Jos kursori on annettu _cursor-parametrissa, transaktionhallinta
# hoidetaan jossakin kutsujassa.
#
# Jos kursoria ei ole annettu, luodaan oma kursori. Tässä tapauksessa
# transaktion päättäminen pitää tapahtua saman metodin sisällä.
#
# Jos metodista tehdään kutsuja toisiin metodeihin, käytettävä kursori
# pitää liittää kutsuparametreihin.
#

class SimpleDatabaseObject(DatabaseObject):
    id_column = 'id'
    other_columns = []
    table_name = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self.__class__, k, v)

    @classmethod
    def load_from_database(cls, _id, **kwargs):
        select_columns = [cls.id_column] + cls.other_columns

        my_cursor = _cursor = kwargs.get('_cursor', None)
        row = None
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()
            query = ("SELECT %s FROM %s WHERE %s = %%s" %
                     (', '.join(select_columns),
                      cls.table_name,
                      cls.id_column))
            my_cursor.execute(query, (int(_id),))
            row = my_cursor.fetchone()
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

        new_dict = dict(map(lambda p: (p[1], row[p[0]]),
                            enumerate(select_columns)))
        return cls(**new_dict)

    @classmethod
    def new(cls, **kwargs):
        insert_columns = sorted(set(cls.other_columns) & set(kwargs.keys()))
        select_columns = [cls.id_column] + insert_columns
        insert_values = map(lambda k: kwargs[k], insert_columns)

        insert_columns_string = ', '.join(insert_columns)
        select_columns_string = ', '.join(select_columns)
        
        values_string = ', '.join(map(lambda x: '%s', insert_columns))

        insert_sql = ("""INSERT INTO %s (%s) VALUES (%s) RETURNING %s""" %
                      (cls.table_name, insert_columns_string, values_string, select_columns_string))

        my_cursor = _cursor = kwargs.get('_cursor', None)

        row = None
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()
            my_cursor.execute(insert_sql, (insert_values))

            row = my_cursor.fetchone()
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

        new_dict = dict(map(lambda p: (p[1], row[p[0]]),
                            enumerate(select_columns)))
        return cls(**new_dict)

    @classmethod
    def load_ids(cls, **kwargs):
        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()
            my_cursor.execute("SELECT %s FROM %s ORDER BY %s" %
                        (cls.id_column, cls.table_name, cls.id_column))
            for row in my_cursor.fetchall():
                yield row[0]
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

    def save(self, **kwargs):
        """Tallenna (päivitä) olion tiedot tietokantaan."""

        update_columns = self.__class__.other_columns
        update_columns_string = ', '.join(map(lambda col: "%s = %%s" % (col), update_columns)) 
        update_sql = ("UPDATE %s SET %s WHERE %s = %%s" %
                      (self.__class__.table_name,
                       update_columns_string,
                       self.__class__.id_column))

        update_values = map(lambda name: getattr(self, name), update_columns)
        update_values.append(getattr(self, self.__class__.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = self.__class__.conn.cursor()
            my_cursor.execute(update_sql, update_values)
        except:
            if _cursor is None:
                self.__class__.conn.rollback()
            raise
        else:
            if _cursor is None:
                self.__class__.conn.commit()

    @classmethod
    def delete(cls, _id, **kwargs):
        """Hävitä tietokannasta kohde, joka täsmää annettuun id-arvoon."""

        delete_sql = ("DELETE FROM %s WHERE %s = %%s" % (cls.table_name, cls.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()
            my_cursor.execute(delete_sql, (_id,))
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()
