#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from DatabaseObject import DatabaseObject
from Kommentti import Kommentti
from SimpleDatabaseObject import SimpleDatabaseObject

class Kohde(SimpleDatabaseObject):
    table_name = 'reseptiohjelma.kohde'
    id_column = 'kohde_id'
    other_columns = ['luotu', 'omistaja']

    @classmethod
    def load_from_database(cls, _id, **kwargs):
        select_columns = Kohde.other_columns

        query = ("SELECT %s FROM %s WHERE %s = %%s" %
                 (', '.join(select_columns),
                  Kohde.table_name,
                  Kohde.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        row = None
        super_object = None
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()

            kwargs['_cursor'] = my_cursor
            super_object = super(Kohde, cls).load_from_database(_id, **kwargs)

            my_cursor.execute(query, (int(_id),))
            row = my_cursor.fetchone()
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

        for i, k in enumerate(select_columns):
            setattr(super_object, k, row[i])

        #
        # Jokaiseen kohteeseen voi liittyä kommentti, joten ne voidaan
        # käyttäjän avuksi ladata tässä.
        #
        kommentit = []
        for kommentti_id in Kommentti.load_ids(kohde_id=_id):
            kommentit.append(Kommentti.load_from_database(kommentti_id))

        super_object.kommentit = kommentit

        return super_object

    @classmethod
    def new(cls, **kwargs):
        select_columns = Kohde.other_columns
        select_columns_string = ', '.join(select_columns)

        update_columns = sorted(set(Kohde.other_columns) & set(kwargs.keys()))
        update_columns_string = ', '.join(map(lambda col: "%s = %%s" % (col), update_columns))
        update_values = map(lambda k: kwargs[k], update_columns)

        update_sql = ("UPDATE %s SET %s WHERE %s = %%s RETURNING %s" %
                      (Kohde.table_name,
                       update_columns_string,
                       Kohde.id_column,
                       select_columns_string))

        my_cursor = _cursor = kwargs.get('_cursor', None)

        row = None
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()

            #
            # Kohde-taulu täytetään päätaulun DEFAULT-arvona
            # kutsuttavassa PL/PgSQL-funktiossa hae_kohde(), joten
            # super-metodia on kutsuttava ensin.
            #
            # Tällaista taulurakennetta voi pitää suunnitteluvirheenä,
            # mutta käypähän malliksi monimutkaisesta
            # tietokantaolioabstraktiosta.
            #
            kwargs['_cursor'] = my_cursor
            super_object = super(Kohde, cls).new(**kwargs)

            update_values.append(getattr(super_object, super_object.id_column))

            my_cursor.execute(update_sql, update_values)

            row = my_cursor.fetchone()
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()

        for i, k in enumerate(select_columns):
            setattr(super_object, k, row[i])

        return super_object

    def save(self, **kwargs):
        """Tallenna (päivitä) olion tiedot tietokantaan."""

        update_columns = Kohde.other_columns
        update_columns_string = ', '.join(map(lambda col: "%s = %%s" % (col), update_columns))
        update_sql = ("UPDATE %s SET %s WHERE %s = %%s" %
                      (Kohde.table_name,
                       update_columns_string,
                       Kohde.id_column))

        update_values = map(lambda name: getattr(self, name), update_columns)
        update_values.append(getattr(self, self.__class__.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = self.__class__.conn.cursor()

            #
            # Pitääkö "kohde"-taulu päivittää ennen vai jälkeen
            # päätaulun päivittämisen?
            #
            kwargs['_cursor'] = my_cursor
            super(Kohde, self.__class__).save(self, **kwargs)

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
        delete_sql = ('DELETE FROM %s WHERE %s = %%s' %
                      (Kohde.table_name, Kohde.id_column))

        my_cursor = _cursor = kwargs.get('_cursor', None)
        try:
            if my_cursor is None:
                my_cursor = cls.conn.cursor()

            kwargs['_cursor'] = my_cursor
            super(Kohde, cls).delete(_id, **kwargs)

            my_cursor.execute(delete_sql, (_id,))
        except:
            if _cursor is None:
                cls.conn.rollback()
            raise
        else:
            if _cursor is None:
                cls.conn.commit()
