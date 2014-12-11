
select distinct ptm from sprot_ptms1 where ft like "CARBOHYD";
select distinct ptm from sprot_ptms1 where ft like "LIPID";
select distinct ptm, from_aa from sprot_ptms1 where ft like "MOD_RES";
select distinct ptm from sprot_ptms1 where ft like "CROSSLNK";
select distinct ptm from sprot_ptms1 where ft like "DISULFID";

# este devuelve 510
select distinct ptm, from_aa, to_aa from sprot_ptms1 order by ptm;
# y este 508
select distinct ptm, from_aa from sprot_ptms1 order by ptm;
# o sea que si tomamos en cuenta combinaciones únicas de to-from, aparecen dos más
# ¿Cuáles son? ¿Son las que yo corregí?