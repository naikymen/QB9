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
tabla_cuentas = "trembl_count5"
tabla_ptms = "trembl_ptms5"
file_name = "uniprot_trembl.dat"

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
categories['FROM_RES'] = "varchar(10) NOT NULL"
categories['TO_RES'] = "varchar(10) NOT NULL"
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

# Crear la tabla de cuentas
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

# Crear la tabla de ptms
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

        # Generar y guardar el insert del #AA en la secuencia
        listaq = []
        contenido_aa = count_amino_acids_ext(record.sequence)  # Guardo el dict con partes AA, #AA de la secuencia
        for q in contenido_aa.itervalues():
            listaq.append(str(q))  # y los pongo en una lista
        sql_insert_values_q = ', '.join(listaq)
        cur.execute("INSERT INTO " + tabla_cuentas + " VALUES ('"
                    + record.accessions[0] + "', '"
                    + record.organism_classification[0] + "', "
                    + str(record.sequence_length)
                    + ", " + sql_insert_values_q + ")")
        con.commit()

        # Acá empiezo con los features, hay alguno interesante?
        features = record.features  # todo insertar los FTs en otra tabla junto con OC; OX, OR...?
        out = []
        for a in range(0, len(features)):  # guardar los campos "candidato" del FT en una lista llamada out
            out.append(features[a][0])
        interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes

        if interes:  # si interes no está vacía, entonces hay algo para cargar
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

                            # reiniciar PTM y STATUS
                            ptm = ''
                            data['PTM'] = empty_data['PTM']
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
                                data['PTM'] = "S-cysteinyl 3-(oxidosulfanyl)alanine (Cys-Cys)"
                            else:  # pero si no lo es, guardamos la ptm en el campo PTM.
                                if len(ptm) >= 50:  # hay algunas ptms que especifican de mas y no matchean con la lista
                                    if ptm[:49] == "Tryptophyl-tyrosyl-methioninium (Trp-Tyr) (with M":
                                        ptm = "Tryptophyl-tyrosyl-methioninium (Trp-Tyr) (with M-...)"
                                    if ptm[:49] == "Tryptophyl-tyrosyl-methioninium (Tyr-Met) (with W":
                                        ptm = "Tryptophyl-tyrosyl-methioninium (Trp-Tyr) (with W-...)"

                                    if ptm[:53] == "Glycyl lysine isopeptide (Gly-Lys) (interchain with K":
                                        ptm = "Glycyl lysine isopeptide (Gly-Lys) (interchain with K-...)"
                                    if ptm[:53] == "Glycyl lysine isopeptide (Gly-Lys) (interchain with G":
                                        ptm = "Glycyl lysine isopeptide (Lys-Gly) (interchain with G-...)"

                                        #if ptm[:50] == "":
                                        #    ptm = ""
                                        #if ptm[:50] == "":
                                        #    ptm = ""

                                data['PTM'] = ptm

                            listap = []
                            for p in data.itervalues():  # itero los valores de los datos que fui cargando al dict.
                                listap.append(str(p).replace("'", "''"))  # y los pongo en una lista
                            sql_insert_values_p = '\'' + \
                                                  '\', \''.join(listap) + \
                                                  '\''
                            # Que después uno como van en el INSERT
                            # El insert, en el que reemplazo ' por '', para escaparlas en sql

                            cur.execute(("INSERT INTO " + tabla_ptms + " VALUES (%r);"
                                         % sql_insert_values_p + '\n').replace("\"", '').replace('.', ''))
                            con.commit()
                            # unir los elementos de values con comas
        else:
            # Si, en cambio, la entrada no tiene FT insteresantes, solo cargo los datos generales y defaults
            listar = []
            for r in data.itervalues():
                listar.append(str(r).replace("'", "''"))
            sql_insert_values_r = '\'' + '\', \''.join(listar) + '\''
            cur.execute(("INSERT INTO " + tabla_ptms + " VALUES (%r);"
                         % sql_insert_values_r + '\n').replace("\"", '').replace('.', ''))
            con.commit()

        #if i >= 10000:  # segun uniprot el número de entradas de secuencias es 54247468
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
#output.close()
print('\n')
print(time.time() - start_time)

# """
