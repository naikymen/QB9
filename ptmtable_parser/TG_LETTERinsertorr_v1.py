__author__ = 'nicolas'
# coding=utf-8

from os.path import expanduser
from ordereddict import OrderedDict
import MySQLdb as mdb

database = "ptmdb"
tabla_ptms = "ptm_table_01"
columna_aa_letra = 'TG_LETTER'
letter_tg = []

# Configurar el cursor para la base de datos mysql
con = mdb.connect('localhost', 'nicolas', passwd="nicolaslfp", db=database)
cur = con.cursor()
cur.execute("USE " + database)
cur.execute("SELECT VERSION()")
fetchone = cur.fetchone()
print(str(fetchone) + " --- \n")

# Armar el diccionario AA->A
aa_file = expanduser("~") + '/QB9/QB9-VCS/resources/aminoacidos_v1'
diccionario_aa = OrderedDict()
res = OrderedDict()

with open(aa_file) as aminoa:
    for line in aminoa:
        record = line.replace("\n", '').split(';')
        diccionario_aa[record[2]] = record[0]
print(diccionario_aa.items())

# Cosas que use
# http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html
# http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchall.html
# http://www.tutorialspoint.com/mysql/mysql-update-query.htm

# Traer los posibles TG y iterarlos y actualizar la tabla usando
# el diccionario de arriba para traducir entre nomenclaturas chinpum
cur.execute("select distinct tg from " + tabla_ptms + ";")
for row in cur:
    name_tg = row[0].split('-')
    for target in name_tg:
        letter_tg.append(diccionario_aa[target])
    new_value = "-".join(letter_tg)
    cur.execute('UPDATE ' + tabla_ptms + ' SET ' + columna_aa_letra + '=\'' + new_value + '\' where TG like \'' + row[0] + '\';')
    del letter_tg[:]
cur.execute('commit;')

# """
