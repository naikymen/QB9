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
categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
categories['FT'] = "varchar(200)"  # ACT_SITE, MOD_RES, LIPID, CARBOHYD, DISULFID, CROSSLNK
categories['SQ'] = "varchar(1000)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs...)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT
print(categories.keys())
for o in categories.iteritems():
    print(o[0] + " " + o[1])

#Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
record = empty_record  # este es el diccionario de registros vacío que voy a usar
for o in record.iteritems():
    print(o[0] + " " + o[1])


i = 0
line = sprot.readline()
print(i)

# todo esto no anda
while i <= 50:  # mientras la linea no sea la "última", o sea, el fin del archivo.
    for cat in categories.iterkeys():
        if line[:2] == cat:
            record[cat] = line[5:-1]
            line = sprot.readline()
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += ' --- ' + line[5:-1]  # agrega su contenido con un separador
                line = sprot.readline()  # y cambia a una nueva linea
    if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//" hacer un INSERT
        print(record.items)
        record = empty_record
    print(i)
    i += 1

# """