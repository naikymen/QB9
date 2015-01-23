#SELECT ptm, inumber FROM ptmdb.sprot_ptms1 where ft not like 'NOFT' and ptm like '%methioninium%';
select note, count(*) from sprot_ptms2 where note not like "%CAR%" group by note;