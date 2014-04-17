# coding=utf-8
__author__ = 'nicolas'
ptmlist = open('../ptmlist', 'r')
from collections import OrderedDict
import psycopg2

categories = OrderedDict()  # las categorías están en un diccionario con su type de postgresql, dsp los cambio
categories['ID'] = "text"
categories['AC'] = "text"
categories['FT'] = "text"
categories['TG'] = "text"
categories['PA'] = "text"
categories['PP'] = "text"
categories['CF'] = "text"
categories['MM'] = "text"
categories['MA'] = "text"
categories['LC'] = "text"
categories['TR'] = "text"
categories['KW'] = "text"
categories['DR'] = "text"

items = categories.items()
print("\n    " + str(categories.items())[2:-2].replace("'", '').replace("),", "").replace(",", "").replace(" (", "\n    "))

"""conn = psycopg2.connect("dbname=test user=naikymen")
cur = conn.cursor()
cur.execute("SELECT * FROM ptm_table")
print(cur.fetchall())"""