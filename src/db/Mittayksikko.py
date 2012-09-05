import psycopg2
from SimpleDatabaseObject import SimpleDatabaseObject

class Mittayksikko(SimpleDatabaseObject):
    table_name = 'reseptiohjelma.mittayksikko'
    id_column = 'nimi'
    other_columns = ['tyyppi', 'perusyksikko', 'kerroin']
