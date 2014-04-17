# coding=utf-8
__author__ = 'nicolas'
from psycopg2 import *
import psycopg2
from collections import OrderedDict

ptmlist = open('../ptmlist', 'r')

categories = OrderedDict()  # las categorías están en un diccionario con su type de postgresql, dsp los cambio
categories['ID'] = "varchar(80) PRIMARY KEY"
categories['AC'] = "varchar(80)"
categories['FT'] = "varchar(80)"
categories['TG'] = "varchar(80)"
categories['PA'] = "varchar(80)"
categories['PP'] = "varchar(80)"
categories['CF'] = "varchar(80)"
categories['MM'] = "varchar(80)"
categories['MA'] = "varchar(80)"
categories['LC'] = "varchar(80)"
categories['TR'] = "varchar(80)"
categories['KW'] = "varchar(80)"
categories['DR'] = "varchar(80)"

conn = psycopg2.connect("dbname=test user=naikymen")
cur = conn.cursor()
cur.execute("SHOW server_version;")
print cur.fetchall()

#variables del insert
sql_insert_values = ''
sql_insert_columns = ''

#crear la tabla
#table_def = str(categories.items())[2:-2].replace("'", '').replace("),", "").replace(",", "").replace(" (", ", ")
#print("CREATE TABLE IF NOT EXISTS test.ptm_table (" + table_def + ");")
#cur.execute("CREATE TABLE IF NOT EXISTS ptm_table (" + table_def + ");")


empty_record = OrderedDict()  # aca voy a meter duplas "nombre de columna" + "valor de campo" de c/linea
for gato in categories:  # para cada categoría
    empty_record[gato] = 'null'  # agregarla al registro y llenar el campo con el valor por defecto
record = empty_record  # defino así el diccionario de registros vacío

line = ptmlist.readline()  # comienzo a contar lineas, asigno el valor de la primera a "line"
i = 0

while line != '':  # mientras la linea no sea la "última", o sea, el fin del archivo.
    if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//" hacer un INSERT
        sql_insert_columns = str(record.keys())[1:-1].replace("'", "")
        sql_insert_values = str(record.values())[1:-1].replace("\"", "\'")
        cur.execute("INSERT INTO test.ptm_table VALUES (" + sql_insert_values + ");")  # PERO NO ANDA!!!!!!
        i += 1  # contar PTMs separadas por la doble barra "//".
        record = empty_record  # después del insert, vaciar el registro.
        line = ptmlist.readline()  # y cambiar de linea.
    for cat in categories.iterkeys():  # toma cada elemento de categoria (en orden)
        if line[:2] == cat:  # y si la linea corresponde a la categoria
            record[cat] = line[5:-1].replace("'", "''")  # agrega su contenido al registro para esa categoria
            line = ptmlist.readline()  # y cambia a una nueva linea
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += ' --- ' + line[5:-1]  # agrega su contenido con un separador
                line = ptmlist.readline()  # y cambia a una nueva linea
    # si la linea está vacía, es porque llegó al final del archivo y el while termina

# antes el registro lo escribí así
#record_cero = {'ID': dummy, 'AC': dummy, 'FT': dummy, 'TG': dummy, 'PA': dummy,
#    'PP': dummy, 'CF': dummy, 'MM': dummy, 'MA': dummy, 'LC': dummy, 'TR': dummy, 'KW': dummy, 'DR': dummy}"""

cur.execute("SELECT * FROM test.ptm_table")
cur.fetchall()