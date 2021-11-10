psql -U postgres -d world -c "
EXPLAIN ANALYZE
select *
from sitio2 s1, sitio2 s2
where s1.countrycode = s2.countrycode
and s1.entidad like 'a%' and s2.entidad like 'b%'
limit 100
"

psql -U postgres -d world -c "
DROP INDEX code_index;
"

psql -U postgres -d world -c "
DROP INDEX code_index;
"

-- SIN INDICE

-- Password for user postgres:
--                                                            QUERY PLAN
-- --------------------------------------------------------------------------------------------------------------------------------
--  Limit  (cost=0.00..4.14 rows=100 width=50) (actual time=0.036..0.411 rows=100 loops=1)
--    ->  Nested Loop  (cost=0.00..53530877.55 rows=1291943472 width=50) (actual time=0.035..0.402 rows=100 loops=1)
--          Join Filter: (s1.countrycode = s2.countrycode)
--          Rows Removed by Join Filter: 52
--          ->  Seq Scan on sitio2 s2  (cost=0.00..19531.00 rows=50470 width=25) (actual time=0.017..0.017 rows=1 loops=1)
--                Filter: (entidad ~~ 'b%'::text)
--                Rows Removed by Filter: 4
--          ->  Materialize  (cost=0.00..19884.29 rows=70658 width=25) (actual time=0.014..0.352 rows=152 loops=1)
--                ->  Seq Scan on sitio2 s1  (cost=0.00..19531.00 rows=70658 width=25) (actual time=0.007..0.316 rows=152 loops=1)
--                      Filter: (entidad ~~ 'a%'::text)
--                      Rows Removed by Filter: 2153
--  Planning Time: 0.566 ms
--  Execution Time: 0.455 ms
-- (13 rows)


-- CON INDICE

-- Password for user postgres:
--                                                                QUERY PLAN
-- -----------------------------------------------------------------------------------------------------------------------------------------
--  Limit  (cost=0.42..0.88 rows=100 width=50) (actual time=0.063..0.503 rows=100 loops=1)
--    ->  Nested Loop  (cost=0.42..5879103.75 rows=1291943472 width=50) (actual time=0.062..0.493 rows=100 loops=1)
--          ->  Seq Scan on sitio2 s2  (cost=0.00..19531.00 rows=50470 width=25) (actual time=0.021..0.022 rows=1 loops=1)
--                Filter: (entidad ~~ 'b%'::text)
--                Rows Removed by Filter: 4
--          ->  Index Scan using code_index on sitio2 s1  (cost=0.42..112.18 rows=392 width=25) (actual time=0.037..0.450 rows=100 loops=1)
--                Index Cond: (countrycode = s2.countrycode)
--                Filter: (entidad ~~ 'a%'::text)
--                Rows Removed by Filter: 1470
--  Planning Time: 1.052 ms
--  Execution Time: 0.574 ms
-- (11 rows)



psql -U postgres -d world -c "
SELECT c.code, 
CASE 
    WHEN c.population IS NULL OR c.population = 0
    THEN 1
    ELSE c.population
    END population_alias, 
c.gnp, site.count_sites
FROM country c
LEFT JOIN (
    SELECT countrycode, count(*) count_sites 
    FROM sitio2 
    GROUP BY countrycode 
) site
ON c.code = site.countrycode
"