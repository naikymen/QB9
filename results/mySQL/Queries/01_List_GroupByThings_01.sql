#Todas las PTMs donde el From y el To son diferentes, son considerados crosslinks
#select ptm, count(AC) count, FROM_AA, TO_AA, ft from sprot_ptms1 where ft not like "NOFT" and TO_AA not like FROM_AA group by PTM, FROM_AA, TO_AA order by count desc
#into outfile "/tmp/mySQL/01_List_GroupByThings_01.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n';

select ptm, count(AC) count, FROM_AA, TO_AA, from_res, to_res, ft from sprot_ptms1 where ft not like "NOFT" and from_res not like to_res group by PTM, FROM_AA order by count desc;
#into outfile "/tmp/mySQL/01_List_GroupByThings_00.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n';
desc sprot_ptms1;
select ptm, count(AC) count, FROM_AA, TO_AA, ft from sprot_ptms1 where ft not like "NOFT" group by PTM, FROM_AA order by count desc;
#into outfile "/tmp/mySQL/01_List_GroupByThings_02.csv" FIELDS TERMINATED BY '&' ENCLOSED BY '%'LINES TERMINATED BY '\n';

#traer las ptm's que tienen un target no identificado ('?')
#select distinct(ptm) from sprot_ptms1 where (from_res like '?' or to_res like '?') and ft not like 'NOFT';
