__author__ = 'nicolas'
#abrir el archivo que contiene la lista de modificaciones postraduccionales de uniprot
ptmlist = open('../ptmlist', 'r')

PTMID = ''

for line in ptmlist:
    IDline = line.count('ID   ')
    TGline = line.count('TR   ')
    line = line.rstrip('\n')  # quita caracter de nueva linea a la derecha
    print('Category:', line[:2], '  Value: ', line[5:])

    #if IDline == 1:
        #line = line.lstrip('ID   ')  # quita segmento 'ID   ' a la izquierda
        #PTMID = line
    #if TGline == 1: