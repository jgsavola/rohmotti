#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from SimpleDatabaseObject import SimpleDatabaseObject

class Kommentti(SimpleDatabaseObject):
    table_name = 'reseptiohjelma.kommentti'
    id_column = 'kommentti_id'
    other_columns = ['kohde_id', 'teksti', 'kuva', 'aika']

    @classmethod
    def prepare_bytea(cls, data):
        return None if data is None else psycopg2.Binary(data)

    @classmethod
    def load_ids(cls, **kwargs):
        select_values = []
        where_string = ''

        if kwargs.get('kohde_id', None) is not None:
            where_string = 'WHERE kohde_id = %s'
            select_values.append(kwargs.get('kohde_id'))

        select_sql = ("SELECT %s FROM %s %s ORDER BY %s" %
                      (cls.id_column, cls.table_name, where_string, cls.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()
            my_cursor.execute(select_sql, select_values)
            for row in my_cursor.fetchall():
                yield row[0]
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

    @classmethod
    def new(cls, **kwargs):
        insert_columns = sorted(set(cls.other_columns) & set(kwargs.keys()))
        select_columns = [cls.id_column] + insert_columns

        #
        # Kikkaile bytea-arvo kuntoon.
        #
        insert_values = map(lambda k: kwargs[k] if k != 'kuva' else cls.prepare_bytea(kwargs[k]), insert_columns)

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

    def save(self, **kwargs):
        """Tallenna (päivitä) olion tiedot tietokantaan."""

        update_columns = self.__class__.other_columns
        update_columns_string = ', '.join(map(lambda col: "%s = %%s" % (col), update_columns))
        update_sql = ("UPDATE %s SET %s WHERE %s = %%s" %
                      (self.__class__.table_name,
                       update_columns_string,
                       self.__class__.id_column))

        update_values = map(lambda name: getattr(self, name) if name != 'kuva' else self.__class__.prepare_bytea(getattr(self, name)), update_columns)
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
