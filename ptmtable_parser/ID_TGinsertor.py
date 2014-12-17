# coding=utf-8
__author__ = 'nicolas'
import MySQLdb as mdb
from os.path import expanduser

con = mdb.connect('localhost', 'nicolas', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE mysql")

aminoacidos_file = expanduser("~") + '/QB9-git/QB9/resources/aminoacidos'
aminoacidos = open(aminoacidos_file)

cur.execute("drop table dist_aa")
cur.execute("create table dist_aa ("
            "nombre varchar(20) NOT NULL,"
            "ID varchar(80) NOT NULL,"
            "TG varchar(40) NOT NULL) "
            "ENGINE=InnoDB")
#cur.execute("alter dist_aa add constraint ptm_id_fk")
#cur.execute("alter dist_aa add constraint fk_nom")

# Defino una funcion de ejecución porque soy vago


def execute(query):
    cur.execute(query)
    con.commit()


aas = []  # Lista de los 20/21 aminoácidos (nombres)
line = aminoacidos.readline()
while line != '':
    aas.append(line[:-1])
    line = aminoacidos.readline()



for nombre in aas:
    nombre = nombre[6:]  # Tomar el nombre largo
    execute("SELECT ID, TG FROM ptm_table WHERE"
            + " TG LIKE '" + nombre + "'"
            + " OR TG LIKE '" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "')")
    """
    variable tg=
    vars(

    )"""
    print("INSERT INTO dist_aa (nombre, ID, TG) VALUES ("
            + "'" + nombre + "',"
            + " (SELECT ID, TG FROM ptm_table WHERE"
            + " TG LIKE '" + nombre + "'"
            + " OR TG LIKE '" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "-%'"
            + " OR TG LIKE '%-" + nombre + "'))")