desc sprot_ptms2;
select PTM, FT from sprot_ptms2 where PTM like "(2-aminosuccinimidyl)acetic acid (Asp-Gly)";
SET SQL_SAFE_UPDATES = 0;
UPDATE sprot_ptms2 SET PTM="(2-aminosuccinimidyl)acetic acid (Asp-Gly)" WHERE PTM like "(2-aminosuccinimidyl)acetic acid (Asp- Gly)";
SET SQL_SAFE_UPDATES = 1;

#(4S)-thiazoline-4-carboxylic acid (Thr- Cys)
SET SQL_SAFE_UPDATES = 0;
UPDATE sprot_ptms2 SET PTM="(4S)-thiazoline-4-carboxylic acid (Thr-Cys)" WHERE PTM like "(4S)-thiazoline-4-carboxylic acid (Thr- Cys)";
SET SQL_SAFE_UPDATES = 1;

# 2-(S-cysteinyl)pyruvic acid O- phosphothioketal
# 5-methyloxazole-4-carboxylic acid (Cys- Thr)
# 5-methyloxazole-4-carboxylic acid (Ser- Thr)
# 5-methyloxazole-4-carboxylic acid (Thr- Thr)
# 5-methyloxazoline-4-carboxylic acid (Ser- Thr)
# 5-methylthiazole-4-carboxylic acid (Asn- Cys)
# Aspartate 1-(chondroitin 4-sulfate)- ester
# Beta-methyllanthionine sulfoxide (Thr- Cys)
# Isoaspartyl cysteine isopeptide (Cys- Asn)
# S-(15-deoxy-Delta12,14-prostaglandin J2- 9-yl)cysteine
# Tele-(1,2,3-trihydroxypropan-2- yl)histidine
# 2-(S-cysteinyl)pyruvic acid O- phosphothioketal

SET SQL_SAFE_UPDATES = 0;
UPDATE sprot_ptms2 SET PTM="2-(S-cysteinyl)pyruvic acid O-phosphothioketal" WHERE PTM like "2-(S-cysteinyl)pyruvic acid O- phosphothioketal";
SET SQL_SAFE_UPDATES = 1;