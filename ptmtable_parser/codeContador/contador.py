# coding=utf-8
__author__ = 'naikymen'

#abrir el archivo que contiene la lista de modificaciones postraduccionales de uniprot
ptmlist = open('../ptmlist', 'r')

#contenedor para las ptm's
ptmlistid = []
ptmlistdupes = []
print("el valor inicial de la lista es: ", ptmlistid, "\n")

#itera en las lienas y en cada una las courrencias de 'ID   '
for line in ptmlist:
    IDline = line.count('ID   ')
    line = line.rstrip('\n')  # quita caracter de nueva linea a la derecha
    line = line[5:]  # quita segmento 'ID   ' a la izquierda
    if IDline == 1:
        if line not in ptmlistid:  # si la linea es de ID y no está en la lista, agregarla a la lista
            #print(line)
            ptmlistid.append(line)
        else:
            ptmlistdupes.append(line)

#imprimir la lista en líneas
for item in ptmlistid:
    print(item)

#contar elementos en la lista
print('Existen', len(ptmlistid), 'tipos de residuos modificados')
print(len(ptmlistdupes), 'son duplicados según el ID')



#cerrar el archivo
ptmlist.close()