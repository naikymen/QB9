# coding=utf-8
__author__ = 'nicolas'
from os.path import expanduser
from ordereddict import OrderedDict
import MySQLdb as mdb

database = "ptmdb"
tabla_ptms = "sprot_ptmtable1"
file_name = "ptmlist2"

# Abrir el archivo con la lista de PTMs y el de output para guardar los querys
ptmlist_file = expanduser("~") + '/QB9/QB9-VCS/' + file_name
# ptmlist = open(ptmlist_file)
output_file = expanduser("~") + '/QB9/QB9-VCS/resources/output.txt'
output = open(output_file, 'w')

# Configurar el cursor para la base de datos mysql
con = mdb.connect('localhost', 'nicolas', passwd="nicolaslfp", db=database)
cur = con.cursor()
cur.execute("SELECT VERSION()")
fetchone = cur.fetchone()
print(str(fetchone) + " --- \n")
output.write(str(fetchone)[1:-2].strip("'")+"\n\n")
cur.execute("USE ptmdb")
print(str(cur.fetchone()) + " --- \n")
cur.execute("SHOW TABLES;")
fetchall = cur.fetchall()
print(fetchall)

# Las categorías están en un diccionario con su type de mysql todo optimizar los campos
categories = OrderedDict()
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

# Variables del insert
sql_insert_values = ''
sql_insert_columns = ''  # no se usa en el insert al final todo borrar
i = 0

# Crear la tabla
table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def = ', '.join(table_def_items)  # definicion de la tabla
# output.write("CREATE TABLE IF NOT EXISTS ptm_table (" + table_def + "); \n")  # guardar el CREATE en output
cur.execute("DROP TABLE " + tabla_ptms + ";")
cur.execute("CREATE TABLE IF NOT EXISTS " + tabla_ptms + " (" + table_def + ") ENGINE=InnoDB;")
con.commit()

# Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
record = empty_record.copy()  # este es el diccionario de registros vacío que voy a usar
# el copy es para que no me los enlace

with open(ptmlist_file) as ptmlist:
    line = ptmlist.readline()  # comienzo a leer lineas, asigno el valor de la primera a "line"
    while line != '':  # mientras la linea no sea la "última", o sea, el fin del archivo.
        if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//" hacer un INSERT
            # output.write(str(record.items()))
            sql_insert_values = '\'' + '\', \''.join(record.itervalues()) + '\''  # unir los values con comas
            # y encerrarlos entre comillas simples
            cur.execute(("INSERT INTO sprot_ptmtable1 VALUES (%r);"
                         % sql_insert_values + '\n').replace("-...", "").replace("\"", '').replace('.', ''))
            con.commit()  # con esto logro que se graben los inserts, sino no anda... pero lo hace re lenteja!
            record = empty_record.copy()
            line = ptmlist.readline()  # y cambiar de linea.
        for cat in categories.iterkeys():  # toma cada elemento de categoria (en orden)
            # if cat == "TG" and cat == line[:2]:
                # record[cat] = line[5:-1]
                # line = ptmlist.readline()
            if cat == "ID" and cat == line[:2]:
                if line.find("with") == -1:
                    record[cat] = line[5:-1].replace("'", "''")
                    line = ptmlist.readline()
                else:
                    record[cat] = line[5:-1].replace("'", "''").split(" (with")[0].split(" (int")[0]
                    line = ptmlist.readline()
            elif line[:2] == cat:  # y si la linea corresponde a la categoria
                record[cat] = line[5:-1].replace("'", "''")  # agrega su contenido al registro para esa categoria
                # todo averiguar por el manejo de las dobles comillas en sql que quiero insertar en mi insert
                line = ptmlist.readline()  # y cambia a una nueva linea
                while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                    record[cat] += ' --- ' + line[5:-1].replace("'", "''")  # agrega su contenido con un separador
                    line = ptmlist.readline()  # y cambia a una nueva linea
        # si la linea está vacía, es porque llegó al final del archivo y el while termina

# Cerrar el kiosko
cur.execute("SHOW WARNINGS")
print("\nWARNINGS: ")
print(cur.fetchall())
if con:
    con.close()

# Ta-da! """