__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt
import time
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE ptmdb")

start_time = time.time()

sprot_file = expanduser("~") + '/QB9_Files/uniprot_sprot.dat'
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

# Counter
i = 0
j = 0
# Container for the list of features
ftlist = []
#  Interesting feature types
ptmrecords = ["MOD_RES", "LIPID", "CARBOHYD", "DISULFID", "CROSSLNK"]
# Non-experimental qualifiers for feature annotations
neqs = ["Probable", "Potential", "By similarity"]  # ¿Y "definitive"?
# Las categorías están en un diccionario con su type de postgresql todo optimizar los campos
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

# Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_data = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_data[gato] = 'NULL'
data = empty_data  # este es el diccionario de registros vacío que voy a usar"""

# Crear la tabla
table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def = ', '.join(table_def_items)  # definicion de la tabla
output = open(output_file, 'w')
output.write("CREATE TABLE IF NOT EXISTS ptm_table (" + table_def + ") ENGINE=InnoDB; \n")  # guardar el CREATE en output
cur.execute("CREATE TABLE IF NOT EXISTS sprot2 (" + table_def + ") ENGINE=InnoDB")
con.commit()

data['STATUS'] = "Experimental"
ptm = ''
out = []
listap = []

with open(sprot_file) as sprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(sprot):
        i += 1
        data = empty_data
        features = record.features  # todo insertar los FTs en otra tabla junto con OC; OX, OR...?
        for a in range(0, len(features)):  # guardar los campos "candidato" del FT en una lista llamada out
            out.append(features[a][0])
        interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes
        if interes:  # si interes no está vacía, entonces hay algo para cargar
            # Acá cargo los datos generales para las PTMs de una proteína/entrada de uniprot (instancias de entradas)
            data['AC'] = record.accessions[0]  # solo el principal, el resto nose.
            data['SQ'] = record.sequence
            data['LENGTH'] = record.sequence_length
            #data['SQi'] = record.seqinfo
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

            # todo evitar duplicados de secuencia, relacion via AC?

            # ahora cargo cada PTM en data (subinstancias de entrada)
            for feature in features:  # iterar los features de la entrada
                if feature[0] in interes:  # si el titulo del FT interesa, proseguir ¡mejora un poco! =D
                    for tipo in interes:  # iterear los tipos interesantes encontrados en el feature
                        if feature[0] in tipo:  # si el feature evaluado interesante, cargar los datos en data[]
                            A = feature[1]  # de el residuo tal (va a ser el mismo que el siguiente si está solo)
                            B = feature[2]  # hacia el otro. OJO hay algunos desconocidos indicados con un "?"
                            C = feature[3]  # este tiene la posta?
                            D = feature[4]  # este aparece a veces? todo wtf?

                            # reiniciar FT, FROM y TO
                            data['FT'] = empty_data['FT']
                            data['FROM_RES'] = empty_data['FROM_RES']
                            data['TO_RES'] = empty_data['TO_RES']
                            # Asignar FT
                            data['FT'] = feature[0]
                            data['FROM_RES'] = A
                            data['TO_RES'] = B
                            # reiniciar


                            # reiniciar PTM y STATUS
                            data['PTM'] = empty_data['PTM']
                            data['STATUS'] = "Experimental"
                            # Asignar STATUS y PTM
                            if C:  # si C (el que tiene el nombre de la PTM y el STATUS) contiene algo
                                for neq in neqs:  # iterar los STATUS posibles
                                    if neq in C:  # si C contiene el STATUS pirulo
                                        data['STATUS'] = neq  # asignar el valor a STATUS
                                        C = C.replace('('+neq+")", '')  # hay que sacar esta porquería
                                        C = C.replace(neq, '')
                                        # hay que sacar esta porquería si no aparece con paréntesis
                                        break  # esto corta con el loop más "cercano" en indentación
                                ptm = ((C.split(" /"))[0].split(';')[0]).\
                                    rstrip(" ").rstrip(".").rstrip(" ")
                                # Obs: a veces las mods tienen identificadores estables que empiezan con "/"
                                # así que hay que sacarlo. y otas cosas desoués de un ";" CHAU.
                                # Ver http://web.expasy.org/docs/userman.html#FT_line
                                # También le saco espacios y puntos al final.
                                if tipo == 'DISULFID':
                                    data['PTM'] = "Disulfide Bridge"
                                else:
                                    data['PTM'] = ptm

                            #if data['AC'] == "P80351":  # si es una de las entradas que tiene problemas, hacer cosas
                            #    print("\n " + tipo + " --- " + data['AC'] + " --- " + data['PTM'])
                            #    print(features)
                            #if data['AC'] == "P80351":  # si es una de las entradas que tiene problemas, hacer cosas
                            #    print(data['FT'])

                            for p in data.itervalues():
                                listap.append(str(p).replace("'", "''"))
                            if len(listap) != 10:
                                print("\n")
                                print(data['AC'])
                                print(listap)
                            sql_insert_values = '\'' + \
                                                '\', \''.join(listap) + \
                                                '\''
                            #if not listap[1]:
                            #    print(listap)
                            #if len(data['FT']) >= 10:
                            #    print("\n")
                            #    print(data['AC'])
                            #    for element in data['FT']:
                            #        print(element)

                            cur.execute(("INSERT INTO sprot2 VALUES (%r);"
                                         % sql_insert_values + '\n').replace("\"", '').replace('.', ''))
                            con.commit()

                            ptm = ''
                            listap = []
                            # unir los elementos de values con comas

        #if i >= 10000:  # el número de entradas (separadas por //) es 542782 verificado con biopython
        #    print("\n")
        #    print(i)
        #    break
# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs..?)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT

# """
output.close()
print('\n')
print(time.time() - start_time)

# """