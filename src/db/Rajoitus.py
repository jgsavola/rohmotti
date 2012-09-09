#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from SimpleDatabaseObject import SimpleDatabaseObject

class Rajoitus(SimpleDatabaseObject):
    table_name = 'rajoitus'
    id_column = 'rajoitus_id'
    other_columns = ['ruokaaine_id', 'henkilo_id', 'rajoitus']
