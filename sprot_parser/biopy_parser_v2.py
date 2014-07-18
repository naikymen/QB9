__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt
import time

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
categories['AC'] = "varchar(20) PRIMARY KEY"  # accesion number
categories['OR'] = "varchar(200)"  # organism
categories['OC'] = "varchar(200)"  # organism classification
categories['OX'] = "varchar(200)"  # taxonomic ID
categories['HO'] = "varchar(200)"  # host organism
# categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
categories['FT'] = "varchar(200)"  # ACT_SITE, MOD_RES, LIPID, CARBOHYD, DISULFID, CROSSLNK
categories['SQ'] = "text(45000)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['SQl'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['SQi'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;

#Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
data = empty_record  # este es el diccionario de registros vacío que voy a usar"""

out = []
ptm = ''
status = ''

with open(sprot_file) as sprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(sprot):
        i += 1
        data['AC'] = record.accessions  # todo insertar el primero y la secuencia+info en una tabla
        data['SQ'] = record.sequence
        data['SQl'] = record.sequence_length
        data['SQi'] = record.seqinfo

        data['OC'] = record.organism_classification
        data['OX'] = record.taxonomy_id
        data['OR'] = record.organism
        data['HO'] = record.host_organism
        data['FT'] = record.features  # todo insertar los FTs en otra tabla junto con OC; OX, OR...?

        for a in range(0, len(data['FT'])):  # guardar los campos "candidato" del FT en una lista llamada out
            out.append(data['FT'][a][0])
        interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes
        if data['AC'][0] == "P02763" or data['AC'][0] == "P19652":
            print(data['FT'])
        if interes:  # si interes no está vacía, entonces hay algo para cargar
        # todo cargar secuencias y ptms por separado? evitar duplicados de secuencia, relacion via AC?
            for feature in data['FT']:  # iterar los features de la entrada
                if feature[0] in interes:  # si el titulo del FT interesa, proseguir ¡mejora un poco! =D
                    for tipo in interes:  # iterear los tipos interesantes encontrados en el feature
                        if feature[0] in tipo:  # si el feature evaluado interesante, imprimir las cosas de ese feature
                            A = feature[1]  # de el residuo tal (va a ser el mismo que el siguiente si está solo)
                            B = feature[2]  # hacia el otro. OJO hay algunos desconocidos indicados con un "?"
                            C = feature[3]  # este tiene la posta?
                            D = feature[4]  # este aparece a veces? todo wtf?
                            status = "OK"
                            ptm = ''
                            if C:
                                for neq in neqs:
                                    if neq in C:
                                        status = neq
                                        C.replace('('+neq+")", '')  # hay que sacar esta porquería
                                        C.replace(neq, '')  # hay que sacar esta porquería si no aparece con paréntesis
                                        break
                                ptm = ((C.split(" /"))[0].split(';')[0]).rstrip(" ").rstrip(".")
                                # Obs: a veces las mods tienen identificadores estables, así que hay que sacarlo. CHAU.
                                # Ver http://web.expasy.org/docs/userman.html#FT_line
        out = []

        if i >= 10000:  # el número de entradas (separadas por //) es 542782 verificado con biopython
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

print('\n')
print(time.time() - start_time)

# """