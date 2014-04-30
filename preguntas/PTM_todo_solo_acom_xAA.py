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
#execute("create table if not exists reactividad ("
#        "nombre varchar(100) not null, total TINYINT, "
#        "solo TINYINT, acomp TINYINT, "
#        "FOREIGN KEY fk_nom(nombre) "
#        "REFERENCES nombresaa(nombre) "
#        "ON DELETE NO ACTION) "
#        "ENGINE=INNODB;")


# Llenar la tabla
for aa in aas:  # Para cada linea en la lista de nombres de aminoácidos
    nombre = aa[6:]  # Tomar el nombre entero
    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            # Conseguir el total de PTMs en las que está involucrado,
            + " TG LIKE '" + nombre + "'"
            + " OR TG LIKE '" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "'")
    fetch = cur.fetchone()
    total = int(str(fetch)[1:-3])

    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            # las PTMs en las que está involucrado con otro residuo de aminoácido y
            + " TG LIKE '" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "'")
    acomp = int(str(cur.fetchone())[1:-3])

    execute("SELECT COUNT(TG) FROM ptm_table WHERE"
            # las PTMs en las que solamente se modifica este residuo
            + " TG LIKE '" + nombre + "'")
    solo = int(str(cur.fetchone())[1:-3])

    execute("INSERT INTO reactividad (nombre, total, solo, acomp) "#
            # guardar en la tabla de reactividades los 3 valores obtenidos
            "VALUES('" + nombre + "', " + str(total) + ", " + str(solo) + ", " + str(acomp) + ")")

# Chauchas """