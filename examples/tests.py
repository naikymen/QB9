# coding=utf-8
__author__ = 'nicolas'
ptmlist = open('../ptmlist', 'r')
from collections import OrderedDict

categories = (  # lista del conjunto de categorías posibles
    'ID',
    'AC',
    'FT',
    'TG',
    'PA',
    'PP',
    'CF',
    'MM',
    'MA',
    'LC',
    'TR',
    'KW',
    'DR',
)

i = 0
dummy = ''
record = OrderedDict()

print(record)

for cat in categories:  # para cada categoría
    record[cat] = i  # agregarla al registro y llenar el campo con el valor por defecto
    i += 1

for key in record.iterkeys():
    print(key)