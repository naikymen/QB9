# coding=utf-8
__author__ = 'Nicolete'
from os.path import expanduser
import sys
from ordereddict import OrderedDict
import MySQLdb as mdb

sprot_file = expanduser("~") + '/QB9_Files/uniprot_sprot.dat'
sprot = open(sprot_file)
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'
output = open(output_file, 'w')

#Las categorías están en un diccionario con su type de postgresql todo optimizar los campos
categories = OrderedDict()
categories['AC'] = "varchar(200) PRIMARY KEY"  # accesion number
categories['OC'] = "varchar(200)"  # organism classification
# categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
categories['FT'] = "varchar(200)"  # ACT_SITE, MOD_RES, LIPID, CARBOHYD, DISULFID, CROSSLNK
categories['SQ'] = "varchar(1000)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
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
record = empty_record  # este es el diccionario de registros vacío que voy a usar
#for o in record.iteritems():
#    print(o[0] + " " + o[1])


i = 0
line = sprot.readline()

# todo saqué el campo de comentarios porque no pude procesar el texto para evitar las 4 lineas de copyright etc...
# la verdad debería mirar mejor los campos, cuáles están cuáles no...
while i <= 1000:
    for cat in categories.iterkeys():
        if line[:2] == cat:  # si la linea es de la categoria evaluada
            if cat == "SQ":  # si esa categoria es la de la secuencia
                record[cat] = line[0:-1] + " -_- "  # guardarla primera linea, agergar el separador
                line = sprot.readline()
                while line[:2] == "  ":  # y mientras no se especifique el campo, pasa con los de la secuencia
                    record[cat] += " " + line[5:-1]  # grabar la linea de secuencia en el campo SQ
                    line = sprot.readline()
            if line[:2] == cat:
                record[cat] = line[5:-1]
                line = sprot.readline()
                while line[:2] == cat:
                    record[cat] += ' -_- ' + line[5:-1]
                    line = sprot.readline()
    if line[:2] == '//':
        print(record)
        record = empty_record
    line = sprot.readline()
    i += 1

"""
i = 0
while i <= 200:
    line = sprot.readline()
    print(line[:-1])
    i += 1
# """