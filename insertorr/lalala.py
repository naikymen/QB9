# coding=utf-8

__author__ = 'nicolas'


from ordereddict import OrderedDict

#Las categorías están en un diccionario con su type de mysql todo optimizar los campos
categories = OrderedDict()
categories['ID'] = "varchar(80) PRIMARY KEY"
categories['AC'] = "varchar(80)"
categories['FT'] = "varchar(80)"
categories['TG'] = "varchar(80)"
categories['PA'] = "varchar(80)"
categories['PP'] = "varchar(80)"
categories['CF'] = "varchar(80)"
categories['MM'] = "varchar(80)"
categories['MA'] = "varchar(80)"
categories['LC'] = "varchar(80)"
categories['TR'] = "varchar(500)"
categories['KW'] = "varchar(80)"
categories['DR'] = "varchar(80)"

empty_record = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_record[gato] = 'null'
record = empty_record.copy()  # este es el diccionario de registros vacío que voy a usar

record['ID'] = 'sarasalarasa'
print(empty_record.items())

del record

try:
    print(record.items())
except:
    print("\n hubo una excepción, no se pudo imprimir record.items \n")
    pass

record = empty_record.copy()
print(record.items())

record.clear()
print(record.items())

record = empty_record.copy()
print(record.items())