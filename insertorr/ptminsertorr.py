# coding=utf-8
__author__ = 'nicolas'
from psycopg2 import *
import psycopg2
from collections import OrderedDict

ptmlist = open('../ptmlist', 'r')

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

conn = psycopg2.connect("dbname=test user=naikymen")
cur = conn.cursor()
sql_table_name = ''
sql_table_query = ''
#for keys in categories.iterkeys():  # armar la parte del el query de columnas y tipos
#    sql_table_query += keys + ' ' + categories[keys] + ', '  # todo resolver problema con los separadores en CREATE
#cur.execute("CREATE TABLE IF NOT EXISTS " + sql_table_name + sql_table_query)  # todo averiguar como era el CREATE
#sql_insert_values = ''

empty_record = OrderedDict()  # aca voy a meter duplas "nombre de columna" + "valor de campo" de c/linea
for gato in categories:  # para cada categoría
    empty_record[gato] = ''  # agregarla al registro y llenar el campo con el valor por defecto
record = empty_record  # defino así el diccionario de registros vacío

line = ptmlist.readline()  # comienzo a contar lineas, asigno el valor de la primera a "line"
i = 0

while line != '':  # mientras la linea no sea la "última", o sea, el fin del archivo.
    if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//"
        #for value in record.itervalues():  # meter cada valor en el registro
        #    sql_insert_values += ', ' + str(value)  # todo resolver problema con los separadores en INSERT
        #cur.execute("INSERT INTO ptm_table VALUES (" + sql_insert_values + ')')  # ejecutar el insert
        i += 1  # contar PTMs separadas por la doble barra "//".
        for key in record.iterkeys():  # un print. Obs: este record está ordenado ¿útil para hacer el INSERT?
            print(key + ' (PTM ' + str(i) + ')' + ':\n' + record[key])
        record = empty_record  # después del insert, vaciar el registro.
        line = ptmlist.readline()  # y cambiar de linea.
    for cat in categories.iterkeys():  # toma cada elemento de categoria (en orden)
        if line[:2] == cat:  # y si la linea corresponde a la categoria
            record[cat] = line[5:-1]  # agrega su contenido al registro para esa categoria
            line = ptmlist.readline()  # y cambia a una nueva linea
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += '\n' + line[5:-1]  # agrega su contenido con el separador de nueva linea, puede ser otro
                line = ptmlist.readline()  # y cambia a una nueva linea
    # si la linea está vacía, es porque llegó al final del archivo y el while termina

# antes el registro lo escribí así
#record_cero = {'ID': dummy, 'AC': dummy, 'FT': dummy, 'TG': dummy, 'PA': dummy,
#    'PP': dummy, 'CF': dummy, 'MM': dummy, 'MA': dummy, 'LC': dummy, 'TR': dummy, 'KW': dummy, 'DR': dummy}"""