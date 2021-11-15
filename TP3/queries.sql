psql -U postgres -d world -c "
EXPLAIN ANALYZE
select *
from sitio2 s1, sitio2 s2
where s1.countrycode = s2.countrycode
and s1.entidad like 'a%' and s2.entidad like 'b%'
limit 100
"

psql -U postgres -d world -c "
CREATE INDEX code_index ON sitio2 USING gin (to_tsvector('english', countrycode))
"

psql -U postgres -d world -c "
DROP INDEX code_index;
"



psql -U postgres -d world -c "
select * from pg_opclass where opcname = 'gin_trgm_ops';
"