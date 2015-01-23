__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
from Bio import SwissProt
import time
import MySQLdb as mdb

# Establecer el tiempo de inicio del script
start_time = time.time()

# Variables del script
database = "ptmdb"
tabla_cuentas = "sprot_count2"
tabla_ptms = "sprot_ptms2"
file_name = "uniprot_sprot.dat"
desde = 0
hasta = 170  # Hay 542782 entradas de AC??
este = 167

# Abrir el .dat de uniprot
uniprot_file = expanduser("~") + '/QB9_Files/' + file_name
output_file = expanduser("~") + '/QB9-git/QB9/resources/output.txt'

# Interesting feature types
ptmrecords = ["MOD_RES", "LIPID", "CARBOHYD", "DISULFID", "CROSSLNK"]
# Non-experimental qualifiers for feature annotations
neqs = ["Probable", "Potential", "By similarity"]  # Y "Experimental"
# Las categorías están en un diccionario con su type de mysql todo volar
categories = OrderedDict()
categories['AC'] = "varchar(30) NOT NULL"  # accesion number
categories['FT'] = "varchar(30) NOT NULL"
categories['STATUS'] = "varchar(30) NOT NULL"
categories['PTM'] = "varchar(100) NOT NULL"
categories['NOTE'] = "varchar(100) NOT NULL"

categories['FROM_RES'] = "varchar(10) NOT NULL"
categories['TO_RES'] = "varchar(10) NOT NULL"
categories['FROM_AA'] = "varchar(10) NOT NULL"  # vamo a implementar el target directamente!!!! =D
categories['TO_AA'] = "varchar(10) NOT NULL"

# categories['SQ'] = "text(45000) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;
categories['LENGTH'] = "varchar(200) NOT NULL"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;

categories['ORG'] = "text(500) NOT NULL"  # organism
categories['OC'] = "varchar(30) NOT NULL"  # organism classification, vamos solo con el dominio
categories['OX'] = "varchar(200) NOT NULL"  # taxonomic ID
categories['HO'] = "text(500)"  # host organism
categories['inumber'] = "varchar(200) NOT NULL"
# categories['CC'] = "varchar(200)"  # comments section, nos interesa el campo "PTM"
# categories['SQi'] = "varchar(200)"  # SQ   SEQUENCE XXXX AA; XXXXX MW; XXXXXXXXXXXXXXXX CRC64;

# Defino un diccionario modelo donde cargar los valores que voy a extraer de la lista
empty_data = OrderedDict()
for gato in categories:  # usando las keys de categories y un valor por defecto todo vacío no es nulo ¿cómo hago?
    empty_data[gato] = 'NOFT'
empty_data['FROM_RES'] = '?'
empty_data['TO_RES'] = '?'
empty_data['FROM_AA'] = '?'
empty_data['TO_AA'] = '?'
data = empty_data.copy()  # este es el diccionario de registros vacío que voy a usar

# Variables del loop
i = 0
j = 0
ptm = ''
out = []
listap = []
listar = []
olista = []
interes = []
# El loop
with open(uniprot_file) as uniprot:  # esto me abre y cierra el archivo al final
    for record in SwissProt.parse(uniprot):  # parseando los records de uniprot
        i += 1
        if i%1000 == 0:
            print(i)
        data = empty_data.copy()  # en vez de vaciar el diccionario, le asigno el dafault sin enlazarlo al vacío
        sequence = record.sequence
        # Acá cargo los datos generales para las PTMs de una proteína/entrada de uniprot (instancias de entradas)
        # tienen que cargarse en el orden de las columnas en la ptmdb y el del insert
        data['AC'] = record.accessions[0]  # solo el principal, el resto nose.
        data['LENGTH'] = record.sequence_length  # todo acá hay un problema? no entran las de mas de 999 residuos?
        data['ORG'] = record.organism  # el bicho
        data['OC'] = record.organism_classification[0]  # el dominio del bicho
        data['OX'] = record.taxonomy_id[0]  # Id taxonomica del bicho

        del olista[:]
        if not record.host_organism:
            data['HO'] = 'No host'
        else:
            for o in record.host_organism:
                olista.append((o.split(";"))[0])
            data['HO'] = ', '.join(olista)  # y esto el host del virus ¿o parásito?

        data['inumber'] = str(i)  # solo para debuguear =) ver hasta donde llegó

        # Acá empiezo con los features, hay alguno interesante?
        features = record.features  # todo insertar los FTs en otra tabla junto con OC; OX, OR...?
        del out[:]
        del interes[:]
        for a in range(0, len(features)):  # guardar los campos "candidato" del FT en una lista llamada out
            out.append(features[a][0])
        interes = list(set(out).intersection(ptmrecords))  # armar un set con los interesantes y hacerlo lista interes
        if i == este:  # si interes no está vacía, entonces hay algo para cargar
            print(features)
                            # unir los elementos de values con comas
        if i >= hasta:  # segun uniprot el número de entradas de secuencias es 54247468
            # print("\n")
            # print(i)
            break
# The sequence counts 60 amino acids per line, in groups of 10 amino acids, beginning in position 6 of the line.
# http://www.uniprot.org/manual/
# General Annotation: cofactores, mass spectrometry data, PTM (complementario al MOD_RES y otras PTMs..?)
# Sequence Annotation (Features): Sites (cleavage sites?), non-standard residue,
# MOD_RES (excluye lipidos, crosslinks y glycanos), lipidación, puente disulfuro, cross-link, glycosylation
# todo consider PE "protein existence", KW contiene "glycoprotein" qué otros?
# todo también dentro de FT

con.commit()
print('\n')
print(time.time() - start_time)

# """
