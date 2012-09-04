#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from DatabaseObject import DatabaseObject

class SimpleDatabaseObject(DatabaseObject):
    id_column = 'id'
    other_columns = []
    table_name = None

    def __init__(self, *args):
        columns = [self.__class__.id_column] + self.__class__.other_columns

        for i, v in enumerate(args):
            setattr(self.__class__, columns[i], v)

    @classmethod
    def load_from_database(cls, _id):
        row = None
        try:
            cur = cls.conn.cursor()
            query = ("SELECT %s FROM %s WHERE %s = %%s" %
                     (', '.join([cls.id_column] + cls.other_columns),
                      cls.table_name,
                      cls.id_column))
            cur.execute(query, (int(_id),))
            row = cur.fetchone()
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

        return cls(*row)

    @classmethod
    def new(cls, *args):
        insert_columns = cls.other_columns
        select_columns = [cls.id_column] + cls.other_columns
        insert_values = args

        insert_columns_string = ', '.join(insert_columns)
        select_columns_string = ', '.join(select_columns)
        
        values_string = ', '.join(map(lambda x: '%s', insert_columns))

        insert_sql = ("""INSERT INTO %s (%s) VALUES (%s) RETURNING %s""" %
                      (cls.table_name, insert_columns_string, values_string, select_columns_string))

        row = None
        try:
            cur = cls.conn.cursor()
            cur.execute(insert_sql, (insert_values))

            row = cur.fetchone()
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

        return cls(*row)

    @classmethod
    def load_ids(cls):
        try:
            cur = cls.conn.cursor()
            cur.execute("SELECT %s FROM %s ORDER BY %s" %
                        (cls.id_column, cls.table_name, cls.id_column))
            for row in cur.fetchall():
                yield row[0]
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

    def save(self):
        """Tallenna (päivitä) olion tiedot tietokantaan."""

        update_columns = self.__class__.other_columns
        update_columns_string = ', '.join(map(lambda col: "%s = %%s" % (col), update_columns)) 
        update_sql = ("UPDATE %s SET %s WHERE %s = %%s" %
                      (self.__class__.table_name,
                       update_columns_string,
                       self.__class__.id_column))

        update_values = map(lambda name: getattr(self, name), update_columns)
        update_values.append(getattr(self, self.__class__.id_column))

        print update_sql

        try:
            cur = self.__class__.conn.cursor()
            cur.execute(update_sql, update_values)
        except:
            self.__class__.conn.rollback()
            raise
        else:
            self.__class__.conn.commit()

    @classmethod
    def delete(cls, _id):
        """Hävitä kohde tietokannasta, joka täsmää annettuun id-arvoon."""

        delete_sql = ("DELETE FROM %s WHERE %s = %%s" % (cls.table_name, cls.id_column))

        try:
            cur = cls.conn.cursor()
            cur.execute(delete_sql, (_id,))
        except:
            cls.conn.rollback()
            raise
        else:
            cls.conn.commit()

    # def delete(self):
    #     """Apumetodi: hävitä kohde, johon self viittaa."""
    #
    #     self.__class__.delete(self, getattr(self, self.__class__.id_column))
