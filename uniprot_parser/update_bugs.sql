desc sprot_ptms2;
select PTM, FT from sprot_ptms2 where PTM like "(2-aminosuccinimidyl)acetic acid (Asp-Gly)";
SET SQL_SAFE_UPDATES = 0;
UPDATE sprot_ptms2 SET PTM="(2-aminosuccinimidyl)acetic acid (Asp-Gly)" WHERE PTM like "(2-aminosuccinimidyl)acetic acid (Asp- Gly)";
SET SQL_SAFE_UPDATES = 1;