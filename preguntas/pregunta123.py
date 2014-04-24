# coding=utf-8
__author__ = 'nicolas'
import MySQLdb as mdb

# me conecto a la base de datos y configuro el cursor para mysql
con = mdb.connect('localhost', 'nicolas', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE mysql")

# Defino una funcion de ejecución porque soy vago


def execute(query):
    cur.execute(query)
    result = cur.fetchall()
    for res in result:
        lista = list(res)
        output = ''
        for item in reversed(lista):
            output += '    ' + str(item)
        print(output.lstrip('    '))


# pregunta: ¿En qué aa se producen las modificaciones postraduccionales de la lista?
execute("SELECT ID, TG FROM ptm_table GROUP BY TG")

# pregunta: ¿Cuántas PTMs hay por aminoácido o par de aminoácidos?
execute("SELECT TG, COUNT(ID) FROM ptm_table GROUP BY TG;")

# pregunta: ¿Cuántas PTMs hay por aminoácido? De a dos o no...
execute("SELECT TG, COUNT(ID) FROM ptm_table GROUP BY TG;")
con.close()