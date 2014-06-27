__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt

sprot_file = expanduser("~") + '/QB9_Files/uniprot_sprot.dat'
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

#  Counter
i = 0
#  Container for the list of features
ftlist = []
#  Interesting feature types
ptmrecords = ["MOD_RES", "LIPID", "CARBOHYD", "DISULFID", "CROSSLNK"]
#  Non-experimental qualifiers for feature annotations
neqs = ["Probable", "Potential", "By similarity"]
#Las categorías están en un diccionario con su type de postgresql todo optimizar los campos
categories = OrderedDict()
categories['AC'] = "varchar(200) PRIMARY KEY"  # accesion number
categories['OC'] = "varchar(200)"  # organism classification
categories['OX'] = "varchar(200)"  # organism classification
# categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
categories['FT'] = "varchar(200)"  # ACT_SITE, MOD_RES, LIPID, CARBOHYD, DISULFID, CROSSLNK
categories['SQ'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['SQl'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['SQi'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;


"""
with open(sprot_file) as sprot:
    for record in SwissProt.parse(sprot):
        i += 1
        print(record.sequence)
        for a in record.features:
            print(a)
        if i > 1000:
            break
"""

with open(sprot_file) as sprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(sprot):
        i += 1
        AC = record.accessions
        print("\nhola " + str(AC))
        OC = record.organism_classification
        OX = record.taxonomy_id
        FT = record.features
        print("\n" + str(FT))
        for feature in FT:
            for tipo in ptmrecords:  # iterear las tipos interesantes
                if feature[0] in tipo:  # si el feature evaluado interesante, imprimir las cosas de ese feature
                    print("--- " + tipo)
                    print("Between " + str(feature[1]) + " and " + str(feature[2]))
                    print(feature[3])
        SQ = record.sequence
        print(SQ)
        SQl = record.sequence_length
        print("Sequence length " + str(SQl))
        SQi = record.seqinfo

        if i > 1000:
            break



# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs...)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT
# print(categories.keys())
# for o in categories.iteritems():
#    print(o[0] + " " + o[1])

#Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
record = empty_record  # este es el diccionario de registros vacío que voy a usar"""