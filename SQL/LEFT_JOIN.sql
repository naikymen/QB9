# SQL LEFT JOIN Keyword
# Returns all rows from the left table (table1), with the matching rows in the right table (table2). The result is NULL in the right side when there is no match.
# SELECT column_name(s)
# FROM table1
# LEFT JOIN table2
# ON table1.column_name=table2.column_name;

select ptm_table.id, sprot_ptms0.ptm from ptm_table LEFT JOIN sprot_ptms0 ON ptm_table.id=sprot_ptms0.ptm;