# coding=utf-8
__author__ = 'nicolas'
from peewee import *
import psycopg2

ptmlist = open('../ptmlist', 'r')

DBNAME = 'ptm_db'
usuario = 'usuariocopado784'
ptm_db = PostgresqlDatabase(DBNAME, user=usuario)
ptm_db.get_conn().set_client_encoding('UTF8')


class PostgresqlModel(Model):
    ID = TextField(unique=True, primary_key=True, help_text='Identifier (FT description); starts a PTM entry')
    AC = TextField(unique=True, help_text='Accession (PTM-xxxx)')
    FT = TextField(help_text='Feature Key')
    TG =
    PA
    PP
    CF
    MM
    MA
    LC
    TR
    KW
    DR


    class Meta:
        database = ptm_db

dummy = ''  # valor por defecto de los campos del registro
record_cero = {}  # un diccionario (el registro) que va a contener los datos para una PTM

categories = {  # lista del conjunto de categorías posibles
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
}

for gato in categories:  # para cada categoría
    record_cero[gato] = dummy  # agregarla al registro y llenar el campo con el valor por defecto


record = record_cero  # defino el diccionario de registros, después me va a servir para vaciarlo

line = ptmlist.readline()  # comienzo a contar lineas, asigno el valor de la primera a "line"
i = 0
while line != '':
    for cat in categories:  # toma cada elemento de categoria
        if line[:2] == cat:  # y si la linea corresponde a la categoria
            record[cat] = line[5:-1]  # agrega su contenido al registro para esa categoria
            line = ptmlist.readline()  # y cambia a una nueva linea
            while line[:2] == cat:  # mientras la linea nueva sea de la misma id que la anterior
                record[cat] += '\n' + line[5:-1]  # agrega su contenido con el separador de nueva linea
                line = ptmlist.readline()  # y cambia a una nueva linea
    if line[:2] == '//':  # y si la nueva linea es un separador de PTMs "//"
        # INSERT INTO ptm's VALUES record ??
        # acá falta el query, que no se hacer todavía
        i += 1  # vamos contando PTMs separadas por la doble barra "//"
        for perro in record:  # un lindo print para ver que anda to-do =)
            print(perro + ' (PTM ' + str(i) + ')' + ':\n' + record[perro])
        record = record_cero  # después del insert, vaciar el registro
        line = ptmlist.readline()  # y cambiar de linea
    # si la linea está vacía, se llegó al final del archivo y el while termina

# antes el registro lo escribí así
#record_cero = {'ID': dummy, 'AC': dummy, 'FT': dummy, 'TG': dummy, 'PA': dummy,
#    'PP': dummy, 'CF': dummy, 'MM': dummy, 'MA': dummy, 'LC': dummy, 'TR': dummy, 'KW': dummy, 'DR': dummy}"""