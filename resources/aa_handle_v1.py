__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict

aa_file = expanduser("~") + '/QB9/QB9-VCS/resources/aminoacidos_v1'
diccionario_aa = OrderedDict()
res = OrderedDict()

with open(aa_file) as aminoa:
    for line in aminoa:
        record = line.replace("\n", '').split(';')
        diccionario_aa[record[2]] = record[0]


print(diccionario_aa.items())

# """