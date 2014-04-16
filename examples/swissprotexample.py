# coding=utf-8

__author__ = 'naikymen'

from Bio import SwissProt
from os.path import expanduser

#handle = open("../resources/uniprot_sprot_fragment_1.dat")
#record = SwissProt.read(handle)

uniprot_sprot_dat = expanduser("~") + '/QB9_Files/uniprot_sprot.dat'
sprot = open(uniprot_sprot_dat)

#descriptions = [record.description for record in SwissProt.parse(handle)]
#len(descriptions)

i = 0
descriptions = []
for record in SwissProt.parse(sprot):
    if not record.description[15:29] == "ncharacterized":  # traer entradas no no caraterizadas
        if i < 5:  # solo 20 elementos en la lista
            descriptions.append(str(record.accessions)[2:-2])  # adjuntar n° de acceso de la entrada sin [' y ']
            i += 1
        else:
            break

for record in descriptions:
    print(record)
print('\n%s' % len(descriptions))