__author__ = 'nicolas'
# coding=utf-8

from ordereddict import OrderedDict
import MySQLdb as mdb


def aminoacids(a):  # Lo mismo que está en aa_handle todo llamarla desde el otro archivo ¿Cómo?
    from os.path import expanduser
    from ordereddict import OrderedDict

    aa_file = expanduser("~") + '/QB9-git/SuperMarioQB9/resources/aminoacidos'
    result = OrderedDict()
    res = OrderedDict()

    with open(aa_file) as aminoa:
        line = aminoa.readline().replace("\n", '')
        while line != '':
            letra = line[0]
            abr = line[2:5]
            nombre = line[6:]
            result[letra] = (abr, nombre)
            line = aminoa.readline().replace("\n", '')
            for o in range(0, len(result)):
                res[result.keys()[o]] = result[result.keys()[o]][a]
    return res


def execute(a):
    cur.execute(a)


def query(b):
    con.query(b)


abcJ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
abc = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
query1 = []
info = OrderedDict()

con = mdb.connect('localhost', 'root', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE ptmdb")

for k in abc:
    query1.append(k)

query2 = 'SUM(' + '), SUM('.join(query1) + ')'
query3 = 'SUM(' + ') + SUM('.join(query1) + ')'

query2 = 'SELECT ' + query2 + ' from count_aa'
query3 = 'SELECT ' + query3 + ' from count_aa'

query(query3)

r = con.store_result()
r = r.fetch_row(maxrows=0)
total = r[0][0]

query(query2)

r = con.store_result()
r = r.fetch_row(maxrows=0)

for i in range(0, 25):
    info[abc[i]] = r[0][i]

j = 0
l = 0

for i, k in info.iteritems():
    print(aminoacids(0)[i] + ", " + str(k*100/total)[0:4] + "%")
    l = l + int(k)
    j = j + (k*100/total)


print("%tot: " + str(j))
print("#TotRes: " + str(l))

query("SELECT COUNT(*) FROM count_aa")
r = con.store_result()
r = r.fetch_row(maxrows=0)
print("#TotSeq: " + str(r[0][0]))

print("En la versión de 2014_03, SwissProt contiene 542782 entradas de secuencia, que suman 193019802 aminoácidos =)")
print("ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases/release-2014_03/knowledgebase/")

#"""