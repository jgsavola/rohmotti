import psycopg2
from Kohde import Kohde
from Kommentti import Kommentti

class Henkilo(Kohde):
    table_name = 'henkilo'
    id_column = 'henkilo_id'
    other_columns = ['nimi', 'tunnus', 'salasana']
