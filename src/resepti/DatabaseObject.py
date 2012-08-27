#!/usr/bin/python

class DatabaseObject:
    #
    # This is the database connection for the class hierarchy.
    #
    conn = None

    #
    # This class method must be called before using any of the database objects.
    #
    @classmethod
    def setDatabaseConnection(cls, conn):
        cls.conn = conn
