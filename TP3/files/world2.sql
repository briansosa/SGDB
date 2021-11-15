--
-- PostgreSQL port of the MySQL "World" database.
--
-- The sample data used in the world database is Copyright Statistics 
-- Finland, http://www.stat.fi/worldinfigures.
--

BEGIN;

--SET client_encoding = 'LATIN1';

COPY city (id, name, countrycode, district, population) FROM stdin;
1	Kabul	AFG	Kabol	1780000
\.

COMMIT;

