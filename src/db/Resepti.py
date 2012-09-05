import psycopg2
from Kohde import Kohde

class Resepti(Kohde):
    id_column = 'resepti_id'
    other_columns = ['nimi', 'valmistusohje']
    table_name = 'reseptiohjelma.resepti'
