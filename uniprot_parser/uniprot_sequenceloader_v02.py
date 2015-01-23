__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt
import time
import MySQLdb as mdb

"""
Fuck!
from ordereddict import OrderedDict
import MySQLdb as mdb

dicc = {}
dictdebug_empty = OrderedDict()
dictdebug = dictdebug_empty
dictdebug['hola'] = 'chau'
print(dictdebug.items())
print(dictdebug_empty.items())
dictdebug_empty.clear()
print(dictdebug_empty.items())
print(dictdebug.items())
"""
# Establecer el tiempo de inicio del script
start_time = time.time()


# Variables del script
database = "ptmdb"
tabla_sequence = "sprot_sq2"
file_name = "uniprot_sprot.dat"
desde = 0
hasta = 542783  # Hay 542782 entradas de AC??

# Conectar a la base de datos
con = mdb.connect('localhost', 'nicolas', passwd="nicolaslfp", db=database)
cur = con.cursor()
cur.execute("SELECT VERSION()")
cur.execute("USE " + database)
print("USE ptmdb;")

# Abrir el .dat de uniprot
uniprot_file = expanduser("~") + '/QB9_Files/' + file_name
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

# Las categorías están en un diccionario con su type de mysql todo volar
categories = OrderedDict()
categories['AC'] = "varchar(30) NOT NULL"  # accesion number
categories['SQ'] = "text(45000) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['LENGTH'] = "varchar(200) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['ORG'] = "text(500) NOT NULL"  # organism
categories['OC'] = "varchar(30) NOT NULL"  # organism classification, vamos solo con el dominio
categories['OX'] = "varchar(200) NOT NULL"  # taxonomic ID
categories['HO'] = "text(500)"  # host organism
categories['inumber'] = "varchar(200) NOT NULL"
# categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
# categories['SQi'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;

# Defino un diccionario modelo donde cargar los valores que voy a extraer de la lista
empty_data = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_data[gato] = ''
data = empty_data.copy()  # este es el diccionario de registros vacío que voy a usar

cur.execute("DROP TABLE " + tabla_sequence + ";")

# Crear la tabla de secuencias
table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def_2 = ', '.join(table_def_items)  # definicion de la tabla
cur.execute("CREATE TABLE IF NOT EXISTS " + tabla_sequence + " (" + table_def_2 + ") ENGINE=InnoDB;")
con.commit()

# Variables del loop
i = 0
j = 0
ptm = ''
out = []
listap = []
listaq = []
listar = []
olista = []
interes = []
with open(uniprot_file) as uniprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(uniprot):  # parseando los records de uniprot
        i += 1
        if i % 1000 == 0:
            print(i)
            con.commit()
        data = empty_data.copy()  # en vez de vaciar el diccionario, le asigno el dafault sin enlazarlo al vacío
        # Acá cargo los datos generales para las PTMs de una proteína/entrada de uniprot (instancias de entradas)
        # tienen que cargarse en el orden de las columnas en la ptmdb y el del insert
        # print(record.accessions[0])
        data['AC'] = record.accessions[0]  # solo el principal, el resto nose.
        data['SQ'] = record.sequence
        data['LENGTH'] = record.sequence_length  # todo acá hay un problema? no entran las de mas de 999 residuos
        data['ORG'] = record.organism  # el bicho
        data['OC'] = record.organism_classification[0]  # el dominio del bicho
        data['OX'] = record.taxonomy_id[0]  # Id taxonomica del bicho

        del olista[:]
        if not record.host_organism:
            data['HO'] = 'No host'
        else:
            for o in record.host_organism:
                olista.append((o.split(";"))[0])
            data['HO'] = ', '.join(olista)  # y esto el host del virus ¿o parásito?

        data['inumber'] = str(i)  # solo para debuguear =) ver hasta donde llegó

        # Si, en cambio, la entrada no tiene FT insteresantes, solo cargo los datos generales y defaults
        del listar[:]
        for r in data.itervalues():
            listar.append(str(r).replace("'", "''"))
        sql_insert_values_r = '\'' + '\', \''.join(listar) + '\''
        if i >= desde:  # para hacerlo en partes
            cur.execute(("INSERT INTO " + tabla_sequence + " VALUES (%r);"
                         % sql_insert_values_r).replace("\"", '').replace('.', ''))

        if i >= hasta:  # segun uniprot el número de entradas de secuencias es 54247468
            # print("\n")
            # print(i)
            break

con.commit()

# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs..?)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT

# output.close()
print('\n')
print(time.time() - start_time)

# """
