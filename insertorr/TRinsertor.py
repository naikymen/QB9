__author__ = 'nicolas'
import MySQLdb as mdb

con = mdb.connect('localhost', 'nicolas', '', '')
cur = con.cursor()
cur.execute("SELECT VERSION()")
print(cur.fetchone())
cur.execute("USE mysql")


cur.execute("DROP TABLE ptm_eukarya")
cur.execute("DROP TABLE ptm_bacteria")
cur.execute("DROP TABLE ptm_archaea")

cur.execute("create table ptm_eukarya ("
            "ID varchar(80) NOT NULL,"
            "AC varchar(20) NOT NULL,"
            "TG varchar(40) NOT NULL) "
            "ENGINE=InnoDB")
#cur.execute("alter ptm_eukarya add constraint ptm_id_fk"
#            "foreign key ptm_id_fk(ID) references ptm_table(ID)"
#            "on delete no action")
cur.execute("alter table ptm_eukarya add constraint ptm_id_fk")
cur.execute("create table ptm_bacteria ( ID varchar(80) NOT NULL, AC varchar(20) NOT NULL, TG varchar(40) NOT NULL) ENGINE=InnoDB")
cur.execute("alter table ptm_bacteria add constraint ptm_id_fk")
cur.execute("create table ptm_archaea ( ID varchar(80) NOT NULL, AC varchar(20) NOT NULL, TG varchar(40) NOT NULL) ENGINE=InnoDB")
cur.execute("alter table ptm_archaea add constraint ptm_id_fk")


cur.execute("delete from ptm_eukarya")
cur.execute("delete from ptm_bacteria")
cur.execute("delete from ptm_archaea")

cur.execute("insert into ptm_eukarya (ID, AC, TG) select ID, AC, TG from ptm_table where TR LIKE '%euka%'")
cur.execute("insert into ptm_bacteria (ID, AC, TG) select ID, AC, TG from ptm_table where TR LIKE '%bacteria%'")
cur.execute("insert into ptm_archaea (ID, AC, TG) select ID, AC, TG from ptm_table where TR LIKE '%archaea%'")
con.commit()