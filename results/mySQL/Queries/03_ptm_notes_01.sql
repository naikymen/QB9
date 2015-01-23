#SELECT ptm, inumber FROM ptmdb.sprot_ptms1 where ft not like 'NOFT' and ptm like '%methioninium%';
select ac, ptm, note, ft, count(*) from sprot_ptms2 group by note;
select distinct ptm from sprot_ptms2 where note like "CAR%";