import psycopg2
from Kohde import Kohde
from Kommentti import Kommentti

class Ruokaaine(Kohde):
    id_column = 'ruokaaine_id'
    other_columns = ['nimi']
    table_name = 'ruokaaine'
