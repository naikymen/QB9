# coding=utf-8
__author__ = 'nicolas'
#abrir el archivo que contiene la lista de modificaciones postraduccionales de uniprot
ptmlist = open('../ptmlist', 'r')

PTMID = ''  #

for line in ptmlist:
    IDline = line.count('ID   ')
    TGline = line.count('TR   ')
    line = line.rstrip('\n')  # quita caracter de nueva linea a la derecha
    if line != '//':
        print('Category:', line[:2], '  Value: ', line[5:])

# INSERT INTO tabla VALUES(IDline