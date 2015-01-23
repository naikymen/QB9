__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt
import time
import MySQLdb as mdb

# Establecer el tiempo de inicio del script
start_time = time.time()

# Variables del script
database = "ptmdb"
tabla_cuentas = "sprot_count2"
tabla_ptms = "sprot_ptms2"
file_name = "uniprot_sprot.dat"

# Armo un diccionario con los AAs que voy a contar
abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
prot_dic = OrderedDict((k, 0) for k in abc)


def count_amino_acids_ext(seq):  # Defino una  función que toma una secuencia y los cuenta
    prot_dic2 = prot_dic
    for aa in prot_dic2:
        prot_dic2[aa] = seq.count(aa)
    return prot_dic2  # y devuelve un dict ordenado con pares AA, #AA


# Conectar a la base de datos
con = mdb.connect('localhost', 'nicolas', passwd="nicolas", db=database)
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE " + database)

# Abrir el .dat de uniprot
uniprot_file = expanduser("~") + '/QB9_Files/' + file_name
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

# Container for the list of features
ftlist = []
# Interesting feature types
ptmrecords = ["MOD_RES", "LIPID", "CARBOHYD", "DISULFID", "CROSSLNK"]
# Non-experimental qualifiers for feature annotations
neqs = ["Probable", "Potential", "By similarity"]  # Y "Experimental"
# Las categorías están en un diccionario con su type de mysql todo optimizar los campos
categories = OrderedDict()
categories['AC'] = "varchar(30) NOT NULL"  # accesion number
categories['FT'] = "varchar(30) NOT NULL"
categories['STATUS'] = "varchar(30) NOT NULL"
categories['PTM'] = "varchar(100) NOT NULL"
categories['FROM_RES'] = "varchar(200) NOT NULL"
categories['TO_RES'] = "varchar(200) NOT NULL"
categories['SQ'] = "text(45000) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['LENGTH'] = "varchar(200) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['ORG'] = "text(500) NOT NULL"  # organism
categories['OC'] = "varchar(30) NOT NULL"  # organism classification, vamos solo con el dominio
categories['OX'] = "varchar(200) NOT NULL"  # taxonomic ID
categories['HO'] = "text(500)"  # host organism
#categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
#categories['SQi'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;

# Defino un diccionario modelo donde cargar los valores que voy a extraer de la lista
empty_data = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_data[gato] = 'NOFT'
data = empty_data  # este es el diccionario de registros vacío que voy a usar

# Crear las tablas
prot_dic_def_items = []
prot_dic_def = OrderedDict((k, 'SMALLINT') for k in abc)
for cat, value in prot_dic_def.items():  # concatenaciones key y valor
    prot_dic_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def = ', '.join(prot_dic_def_items)  # definicion de la tabla
cur.execute("CREATE TABLE IF NOT EXISTS "
            + tabla_cuentas
            + " (AC VARCHAR(30) UNIQUE, OC_ID VARCHAR(30), LENGTH MEDIUMINT,"
            + table_def
            + ") ENGINE=InnoDB")
con.commit()

table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def_2 = ', '.join(table_def_items)  # definicion de la tabla
cur.execute("CREATE TABLE IF NOT EXISTS " + tabla_ptms + " (" + table_def_2 + ") ENGINE=InnoDB")
con.commit()

# Variables del loop
i = 0
j = 0
ptm = ''
out = []
listap = []
listaq = []
listar = []
with open(uniprot_file) as uniprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(uniprot):  # parseando los records de uniprot
        i += 1
        if i > 500:
            data = empty_data
            # Acá cargo los datos generales para las PTMs de una proteína/entrada de uniprot (instancias de entradas)
            data['AC'] = record.accessions[0]  # solo el principal, el resto nose.
            data['SQ'] = record.sequence
            data['LENGTH'] = record.sequence_length
            data['OX'] = record.taxonomy_id
            data['ORG'] = record.organism  # el bicho
            data['OC'] = record.organism_classification[0]  # el dominio del bicho
            if not record.host_organism:
                data['HO'] = 'No host'
            else:
                olista = []
                for o in record.host_organism:
                    olista.append((o.split(";"))[0])
                data['HO'] = ', '.join(olista)  # y esto el host del virus ¿o parásito?

            # Acá empiezo con los features, hay alguno interesante?

            feature = record.features
            out = []
            for a in range(0, len(feature)):  # guardar los campos "candidato" del FT en una lista llamada out
                out.append(feature[a][0])
                print(feature[a][0])
            interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes

        if i > 500:  # segun uniprot el número de entradas de secuencias es 54247468
            print("\n")
            print(i)
            break
# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs..?)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT

# """
#output.close()
print('\n')
print(time.time() - start_time)

# """
