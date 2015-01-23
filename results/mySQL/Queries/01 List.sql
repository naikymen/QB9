select ptm, ft, count(AC) count from sprot_ptms1 where ft not like "NOFT" group by ptm order by count desc;
#into outfile "/tmp/mySQL/01_List.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n';

#select ptm, ft, count(AC) count from sprot_ptms1 where ft not like "NOFT" and STATUS like "Experimental" group by ptm order by count desc into outfile "/tmp/mySQL/01_List_Experimental.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n';
desc sprot_ptms1;