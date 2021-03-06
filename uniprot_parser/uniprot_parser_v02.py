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
desde = 0
hasta = 542785  # Hay 542782 entradas de AC??

# Conectar a la base de datos
con = mdb.connect('localhost', 'nicolas', passwd="nicolaslfp", db=database)
cur = con.cursor()
cur.execute("SELECT VERSION()")
cur.execute("USE " + database)
print("USE ptmdb;")

# Abrir el .dat de uniprot
uniprot_file = expanduser("~") + '/QB9_Files/' + file_name
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

# Interesting feature types
ptmrecords = ["MOD_RES", "LIPID", "CARBOHYD", "DISULFID", "CROSSLNK"]
# Non-experimental qualifiers for feature annotations
neqs = ["Probable", "Potential", "By similarity"]  # Y "Experimental"
# Las categorías están en un diccionario con su type de mysql todo volar
categories = OrderedDict()
categories['AC'] = "varchar(30) NOT NULL"  # accesion number
categories['FT'] = "varchar(30) NOT NULL"
categories['STATUS'] = "varchar(30) NOT NULL"
categories['PTM'] = "varchar(100) NOT NULL"
categories['NOTE'] = "varchar(100) NOT NULL"

categories['FROM_RES'] = "varchar(10) NOT NULL"
categories['TO_RES'] = "varchar(10) NOT NULL"
categories['FROM_AA'] = "varchar(10) NOT NULL"  # vamo a implementar el target directamente!!!! =D
categories['TO_AA'] = "varchar(10) NOT NULL"

# categories['SQ'] = "text(45000) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
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
    empty_data[gato] = 'NOFT'
empty_data['FROM_RES'] = '?'
empty_data['TO_RES'] = '?'
empty_data['FROM_AA'] = '?'
empty_data['TO_AA'] = '?'
data = empty_data.copy()  # este es el diccionario de registros vacío que voy a usar

cur.execute("DROP TABLE " + tabla_ptms + ";")

# Crear la tabla de ptms
table_def_items = []  # lista para concatenaciones de key y valor
for cat, value in categories.items():  # concatenaciones key y valor
    table_def_items.append(cat + ' ' + value)  # guardadaes en la lista
table_def_2 = ', '.join(table_def_items)  # definicion de la tabla

cur.execute("CREATE TABLE IF NOT EXISTS " + tabla_ptms + " (" + table_def_2 + ") ENGINE=InnoDB;")
con.commit()

# Variables del loop
i = 0
j = 0
ptm = ''
out = []
listap = []
listar = []
olista = []
interes = []
# El loop
with open(uniprot_file) as uniprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(uniprot):  # parseando los records de uniprot
        i += 1
        if i%1000 == 0:
            print(i)
        data = empty_data.copy()  # en vez de vaciar el diccionario, le asigno el dafault sin enlazarlo al vacío
        sequence = record.sequence
        # Acá cargo los datos generales para las PTMs de una proteína/entrada de uniprot (instancias de entradas)
        # tienen que cargarse en el orden de las columnas en la ptmdb y el del insert
        data['AC'] = record.accessions[0]  # solo el principal, el resto nose.
        data['LENGTH'] = record.sequence_length  # todo acá hay un problema? no entran las de mas de 999 residuos?
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

        # Acá empiezo con los features, hay alguno interesante?
        features = record.features  # todo insertar los FTs en otra tabla junto con OC; OX, OR...?
        del out[:]
        del interes[:]
        for a in range(0, len(features)):  # guardar los campos "candidato" del FT en una lista llamada out
            out.append(features[a][0])
        interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes
        if interes and i > desde:  # si interes no está vacía, entonces hay algo para cargar
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
                            data['FT'] = 'NOFT'
                            data['FROM_RES'] = '?'
                            data['TO_RES'] = '?'
                            data['FROM_AA'] = '?'
                            data['TO_AA'] = '?'

                            # Asignar FT
                            data['FT'] = feature[0]

                            # Asignar FROM y TO_RES, preparar FROM y TO_AA
                            data['FROM_RES'] = A
                            if type(A) is int:
                                A_res = sequence[int(data['FROM_RES'])-1]
                            else:
                                A_res = '?'

                            data['TO_RES'] = B
                            if type(B) is int:
                                B_res = sequence[int(data['TO_RES'])-1]
                            else:
                                B_res = '?'

                            # reiniciar PTM, NOTE y STATUS
                            ptm = ''
                            data['PTM'] = 'NOFT'
                            data['NOTE'] = 's/n'
                            data['STATUS'] = "Experimental"

                            # Asignar STATUS y PTM
                            if C:  # si C (el que tiene el nombre de la PTM y el STATUS) contiene algo
                                for neq in neqs:  # iterar los STATUS posibles
                                    if neq in C:  # si C contiene el STATUS pirulo
                                        data['STATUS'] = neq  # asignar el valor a STATUS
                                        C = C.replace('(' + neq + ")", '')  # hay que sacar esta porquería
                                        C = C.replace(neq, '')
                                        # hay que sacar esta porquería si no aparece con paréntesis
                                        break  # esto corta con el loop más "cercano" en indentación

                                ptm = ((C.split(" /"))[0].split(';')[0]). \
                                    rstrip(" ").rstrip(".").rstrip(" ")
                                # Obs: a veces las mods tienen identificadores estables que empiezan con "/"
                                # así que hay que sacarlo. y otas cosas después de un ";" CHAU.
                                # También hay CROSSLNKs con otras anotaciones, que los hace aparecer como únicas
                                # al contarlas, pero en realidad son casi iguales todo quizás ocurre con otras?
                                # Ver http://web.expasy.org/docs/userman.html#FT_line
                                # También le saco espacios y puntos al final.
                                # Odio esto del formato... todo no hay algo que lo haga mejor?
                            if tipo == 'DISULFID':  # si el tipo es disulfuro, no hay mucho que decir.
                                ptm = "S-cysteinyl 3-(oxidosulfanyl)alanine (Cys-Cys)"
                                data['FROM_AA'] = 'C'
                                data['TO_AA'] = 'C'
                            else:  # pero si no lo es, guardamos cosas normalmente.
                                # Asignar target residue
                                if A == '?': data['FROM_AA'] = '?'  # Si from es desconocido, asignar ?
                                else: data['FROM_AA'] = A_res  # de lo contrario asignar A_res

                                if B == '?': data['TO_AA'] = '?'  # Si to es desconocido, asignar ?
                                else:
                                    if A == B: data['TO_AA'] = "-"  # Si en cambio to=from, poner un guion en to_aa
                                    else: data['TO_AA'] = B_res  # De otra forma asignar el to_aa (caso crosslnk xej)

                                if ptm.find("with") != -1:  # si la ptm contiene la palabra "with" (caso crosslink)
                                    note = ptm
                                    ptm = ptm.split(" (with")[0].split(" (int")[0]  # recortar
                                    data['NOTE'] = note

                            data['PTM'] = ptm
                            if D != '':
                                data['NOTE'] = D

                            del listap[:]
                            for p in data.itervalues():  # itero los valores de los datos que fui cargando al dict.
                                listap.append(str(p).replace("'", "''"))  # y los pongo en una lista
                            sql_insert_values_p = '\'' + \
                                                  '\', \''.join(listap) + \
                                                  '\''

                            # Que después uno como van en el INSERT
                            # El insert, en el que reemplazo ' por '', para escaparlas en sql

                            cur.execute(("INSERT INTO " + tabla_ptms + " VALUES (%r);"
                                         % sql_insert_values_p).replace("-...", "").replace("\"", '').replace('.', ''))

                            # unir los elementos de values con comas
        if i >= hasta:  # segun uniprot el número de entradas de secuencias es 54247468
            # print("\n")
            # print(i)
            break
# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs..?)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT

con.commit()
print('\n')
print(time.time() - start_time)

# """
