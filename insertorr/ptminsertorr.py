# coding=utf-8
__author__ = 'nicolas'
from os.path import expanduser
import sys
from ordereddict import OrderedDict
#from collections import OrderedDict
import MySQLdb as mdb

ptmlist_file = expanduser("~") + '/QB9-git/QB9/ptmlist'
ptmlist = open(ptmlist_file)
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'
output = open(output_file, 'w')
con = mdb.connect('localhost', 'naikymen', '', 'nicolete')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())


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
categories['TR'] = "varchar(500)"
categories['KW'] = "varchar(80)"
categories['DR'] = "varchar(80)"

#conn = psycopg2.connect("dbname=test user=naikymen")
#cur = conn.cursor()
#cur.execute("SHOW server_version;")
#print cur.fetchall()

#variables del insert
sql_insert_values = '\''
sql_insert_columns = ''

#crear la tabla
table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def = ', '.join(table_def_items)  # definicion de la tabla
#output.write("CREATE TABLE IF NOT EXISTS ptm_table (" + table_def + "); \n")  # guardar el CREATE en output
cur.execute("CREATE TABLE IF NOT EXISTS ptm_table (" + table_def + ")")
con.commit()

empty_record = OrderedDict()  # dicionario para las duplas "nombre de columna" + "valor de campo" de c/linea
for gato in categories:  # defino los keys del diccionario y les asigno un valor x defecto
    empty_record[gato] = 'null'
record = empty_record  # defino así el diccionario de registros vacío que voy a usar

line = ptmlist.readline()  # comienzo a contar lineas, asigno el valor de la primera a "line"
while line != '':  # mientras la linea no sea la "última", o sea, el fin del archivo.
    if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//" hacer un INSERT
        output.write(str(record.items()))
        sql_insert_values = '\'' + '\', \''.join(record.itervalues()) + '\''  # unir los elementos devalues con comas
        output.write(("\nINSERT INTO ptm_table VALUES (%r);" % sql_insert_values + '\n').replace("\"", ''))
        #print(("INSERT INTO ptm_table VALUES (%r);" % sql_insert_values + '\n').replace("\"", ''))
        print(("INSERT INTO ptm_table VALUES (%r);" % sql_insert_values + '\n').replace("\"", ''))
        cur.execute(("INSERT INTO ptm_table VALUES (%r);" % sql_insert_values + '\n').replace("\"", ''))
        con.commit()  # con esto logro que se graben los inserts, sino no anda... pero lo hace re lenteja!
        record = empty_record  # después del insert, vaciar el registro.
        line = ptmlist.readline()  # y cambiar de linea.
    for cat in categories.iterkeys():  # toma cada elemento de categoria (en orden)
        if line[:2] == cat:  # y si la linea corresponde a la categoria
            record[cat] = line[5:-1].replace("'", "''")  # agrega su contenido al registro para esa categoria
            line = ptmlist.readline()  # y cambia a una nueva linea
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += ' --- ' + line[5:-1]  # agrega su contenido con un separador
                line = ptmlist.readline()  # y cambia a una nueva linea
    # si la linea está vacía, es porque llegó al final del archivo y el while termina"""

#Cerrar el kiosko
cur.execute("SHOW WARNINGS")
print(cur.fetchall())
if con:
    con.close()