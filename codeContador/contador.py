__author__ = 'naikymen'

#abrir el archivo que contiene la lista de modificaciones postraduccionales de uniprot
ptmlist = open('../ptmlist', 'r')

#contenedor para las ptm's
ptmlistid = []

#buscar lineas que contengan el ID de la ptm y concatenarlas a la lista ptmlistid
for line in ptmlist:
    lineadeID = line.count('ID   ')
    if lineadeID == 1:
        ptmlistid.append(line)

#imprimir dos los primeros dos elementos porque sí
print(ptmlistid[:2])
ptmlist.close()
