# coding=utf-8
__author__ = 'nicolas'

ptmlist = open('../ptmlist', 'r')

categories = {
}

dummy = ''

categories = (
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

record_cero = {
    'ID': dummy,
    'AC': dummy,
    'FT': dummy,
    'TG': dummy,
    'PA': dummy,
    'PP': dummy,
    'CF': dummy,
    'MM': dummy,
    'MA': dummy,
    'LC': dummy,
    'TR': dummy,
    'KW': dummy,
    'DR': dummy,
}
record = record_cero
"""
for line in ptmlist:
    recordno = 1
    linecat = line[:2]
    if line == "//":  # si cambiamos de PTM
        recordno += 1  # avanzar un registro
        record = record_cero  # y vaciar el registro

    for i in range(0, len(categories)-1):
        if line == categories[i]:
            record[i] = line[5:]
"""

"""
for i in range(0, 12):  # len(categories)-1
    line = ptmlist.readline()
    if line[:2] == categories[i]:
        record[i] = line[5:]
        print(record[i])
"""
i = 0
line = ptmlist.readline().lstrip('\n')
while i < 13:
    print line[:2] + categories [i]
    if line[:2] == categories[i]:  # si la linea corresponde al campo "i"
        print('se guarda ', line[5:], ' en ' + categories[i]) # HACER QUE IMPRIMA EN UNA LINE
        #record[categories[i]] = line[5:]  # guardar sus datos en el campo que corresponde a la categoria
        #print(categories[i] + ' --- ' + record[categories[i]])  # e imprimir la categoria
        line = ptmlist.readline().lstrip('\n')
    i += 1