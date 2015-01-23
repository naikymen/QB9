#desc sprot_ptmtable1;
select id, ft, kw, tg, tg_letter, ac, dr from sprot_ptmtable1;
#into outfile "/tmp/mySQL/02_Table.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n'