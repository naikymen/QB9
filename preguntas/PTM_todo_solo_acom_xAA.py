# coding=utf-8
__author__ = 'nicolas'
import MySQLdb as mdb
from os.path import expanduser

# me conecto a la base de datos y configuro el cursor para mysql
con = mdb.connect('localhost', 'nicolas', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE mysql")

# Abrir el archivo con los nombres completos de los aminoacidos
aminoacidos_file = expanduser("~") + '/QB9-git/QB9/resources/aminoacidos'
aminoacidos = open(aminoacidos_file)

# Defino una funcion de ejecución porque soy vago


def execute(query):
    cur.execute(query)
    con.commit()

# Creat tabla para los nombres de los aminoacidos
#execute("CREATE TABLE IF NOT EXISTS nombresaa ("
#        "nombre varchar(20) PRIMARY KEY, "
#        "corto varchar(3) UNIQUE, "
#        "letra varchar(1) UNIQUE)")

# Llenar la tabla con los nombres
aas = []  # Lista de los 20/21 aminoácidos
line = aminoacidos.readline()
while line != '':
    aas.append(line[:-1])
    #execute("INSERT INTO nombresaa VALUES('" + line[6:-1] + "', '" + line[2:5] + "', '" + line[0] + "')")
    line = aminoacidos.readline()

# Crear la tabla para la "reactividad" de los aminoácidos
#execute("CREATE TABLE IF NOT EXISTS reactividad ("
#        "nombre varchar(20) PRIMARY KEY, "  # Acá puedo poner foreign key?
#        "total TINYINT, "
#        "solo TINYINT, "
#        "acomp TINYINT)")

# Llenar la tabla
solo = 0

for aa in aas:
    print(aa[6:])

# Obtener el total
for aa in aas:
    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            + " TG LIKE '" + aa[6:] + "'"
            + " OR TG LIKE '" + aa[6:] + "-%'"
            + " OR TG LIKE '%-" + aa[6:] + "-%'"
            + " OR TG LIKE '%-" + aa[6:] + "'")
    total = int(str(cur.fetchone())[1:3].rstrip('L'))
    print(str(total) + " -- " + aa[6:])

    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            + " OR TG LIKE '" + aa[6:] + "-%'"
            + " OR TG LIKE '%-" + aa[6:] + "-%'"
            + " OR TG LIKE '%-" + aa[6:] + "'")
    acomp = int(str(cur.fetchone())[1:3].rstrip('L'))
    print(str(acomp) + " -- " + aa[6:])

    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            + " TG LIKE '" + aa[6:] + "'")
    solo = int(str(cur.fetchone())[1:3].rstrip('L'))
    print(str(solo) + " -- " + aa[6:])

# Chauchas """