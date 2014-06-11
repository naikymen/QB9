# coding=utf-8
__author__ = 'Nicolete'
from os.path import expanduser
import sys
from ordereddict import OrderedDict
#from collections import OrderedDict
import MySQLdb as mdb

sprot_file = expanduser("~") + '/QB9-files/sprot.dat'
sprot = open(sprot_file)
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'
output = open(output_file, 'w')
container = []
#Las categorías están en un diccionario con su type de postgresql todo optimizar los campos
categories = OrderedDict()
categories['AC'] = "varchar(80) PRIMARY KEY"  # accesion number
categories['TR'] = "varchar(80)"  # taxonomic range
categories['TL'] = "varchar(80)"  # taxonomic lineage todo revisar los códicos para TR, TL, PTM, etc...
categories['MOD_RES'] = "varchar(80)"  # PTM
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs...)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation


#Defino un modelo de diccionario donde cargar los valores que voy a extraer de la lista
empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
record = empty_record  # este es el diccionario de registros vacío que voy a usar

line = sprot.readline()
while line != '':  # mientras la linea no sea la "última", o sea, el fin del archivo.
    if line[:2] == '//':  # si la nueva linea es un separador de PTMs "//" hacer un INSERT
        print(record.items)
        record = empty_record
    for cat in categories.iterkeys():
        if line[:2] == cat:
            record[cat] = line[5:-1]
            line = sprot.readline()
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += ' --- ' + line[5:-1]  # agrega su contenido con un separador
                line = sprot.readline()  # y cambia a una nueva linea