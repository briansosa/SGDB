--3.1.1
--CREATE DATABASE world;

-- 3.1.3
-- SELECT * FROM city LIMIT 100;
-- SELECT * FROM country LIMIT 100;
-- SELECT * FROM countrylanguage LIMIT 100;


-- CONSULTAS SIMPLES

-- 3.2.1 La poblacion de Argentina

SELECT population FROM country WHERE name = 'Argentina';

-- 3.2.2 Todos los continentes (sin repeticiones)

SELECT DISTINCT continent FROM country;

-- 3.2.3 Nombres de los pases de America del Sur con mas de 15 millones de habitantes

SELECT name FROM country WHERE continent = 'South America' AND population > 15000000;

-- 3.2.4 Nombre y producto bruto de los diez pases con mayor producto bruto (gnp)

SELECT name, gnp FROM country ORDER BY gnp DESC LIMIT 10;

-- 3.2.5 Forma de gobierno y cantidad de paises con dicha forma de gobierno ordenados por cantidad de modo descendente

SELECT governmentform, count(*) count FROM country GROUP BY governmentform ORDER BY count DESC;

-- 3.2.6 Los nombres de los continentes con sus respectivas supercies ordenados de forma descendentes por supercie

SELECT continent, sum(surfacearea) total_surfaceare FROM country GROUP BY continent ORDER BY total_surfaceare DESC; 

-- 3.2.7 Los continentes y la cantidad de paises que los componen de aquellos continentes con mas de 15 pases

SELECT continent, count(name) sum_countries FROM country GROUP BY continent HAVING count(name) > 15;

-- 3.2.8 Idem 3.2.7 pero que los paises que se tengan en cuenta tengan una poblacion de mas de 20 millones de personas

SELECT continent, count(name) sum_countries FROM country WHERE population > 20000000 GROUP BY continent HAVING count(name) > 15;


------

-- SUBQUERIES

-- 3.2 1. >Que hace la siguiente consulta?
-- SELECT name, lifeexpectancy
-- from country
-- where lifeexpectancy = (SELECT min ( lifeexpectancy ) from country)

-- Trae el nombre y el expectativa del país que tiene la menor expectativa de vida

-- 3.2.2 Nombre del pais y la expectativa de vida de el/los pases con mayor y menor expectativa de vida

SELECT name, lifeexpectancy
FROM country
WHERE lifeexpectancy = (SELECT MIN(lifeexpectancy) FROM country);

SELECT name, lifeexpectancy
FROM country
WHERE lifeexpectancy = (SELECT MAX(lifeexpectancy) FROM country);


-- 3.2.3 Nombre de los pases y a~no de independencia que pertenecen al continente del pas que se independizo hace mas tiempo

SELECT name, indepyear
FROM country
WHERE continent = (
    SELECT continent 
        FROM country 
        WHERE indepyear = (SELECT MIN(indepyear) FROM country)
);


-- 3.2.4 Nombres de los continentes que no pertenencen al conjunto de los continentes mas pobres

SELECT continent, sum(gnp) sum_gnp FROM country GROUP BY continent HAVING sum(gnp) > 3000000 ORDER BY sum_gnp ASC;


--------

-- JOINS

-- 3.2.1 Los paises y las lenguas de los paises de Oceania

SELECT c.name, cl.language
FROM country c
INNER JOIN countrylanguage cl ON c.code = cl.countrycode
WHERE c.continent = 'Oceania';


-- 3.2.2 Los paises y la cantidad de lenguas de los paises en los que se habla mas de una lengua (ordenar por cantidad de
-- lenguas de forma descendente)

SELECT c.name, count_languages.count
FROM country c
INNER JOIN (
    SELECT countrycode, count(*) count FROM countrylanguage GROUP BY countrycode HAVING count(*) > 1
) count_languages
ON c.code = count_languages.countrycode
ORDER BY count_languages.count DESC;

-- 3. Las lenguas que se hablan en el continente mas pobre (sin considerar a Antarctica)

SELECT DISTINCT cl.language
FROM countrylanguage cl
INNER JOIN (
    SELECT code FROM country WHERE continent = (
        SELECT continent FROM country WHERE continent <> 'Antarctica' GROUP BY continent ORDER BY sum(gnp) ASC LIMIT 1
    ) 
) codes_continent_poor
ON cl.countrycode = codes_continent_poor.code;

-- 3.2.4 Los nombres de los pases y sus respectivas poblaciones calculadas de formas distintas: 
    -- 1) de acuerdo al campo de la tabla country

SELECT name, population FROM country ORDER BY population DESC;

    -- 2) como suma de las poblaciones de sus ciudades correspondientes

SELECT c.name, countrylanguage.sum_population
FROM country c
INNER JOIN (
    SELECT countrycode, SUM(population) sum_population FROM city GROUP BY countrycode
) countrylanguage
ON c.code = countrylanguage.countrycode
ORDER BY countrylanguage.sum_population DESC;

-- Ademas se pide calcular el porcentaje de poblacion urbana (de las ciudades), ordenar por porcentaje de modo descendente

-- SELECT c.name, countrylanguage.sum_population, city.name city_name, (city.population * 100 / countrylanguage.sum_population) percent_population
-- FROM country c
-- INNER JOIN (
--     SELECT countrycode, SUM(population) sum_population FROM city GROUP BY countrycode
-- ) countrylanguage
-- ON c.code = countrylanguage.countrycode
-- INNER JOIN city ON c.code = city.countrycode
-- ORDER BY c.name;

SELECT c.name, (countrycities.sum_population * 100/ c.population) porcentaje_poblacion_urbana
FROM country c
INNER JOIN (
    SELECT countrycode, SUM(population) sum_population FROM city GROUP BY countrycode
) countrycities
ON c.code = countrycities.countrycode
INNER JOIN city ON c.code = city.countrycode
ORDER BY c.name;



-- 3.3. Ejercicio 3
-- Crear la siguiente tabla de estadsticas (utilizando la informacion de las tablas importadas):
-- Nombre: stats
-- Campos:
--  countrycode: primary key/forign key (tabla country)
--  cant lenguas: cantidad de lenguas que se hablan en el pas
--  pop urbana: cantidad total de habitantes en las ciudades del pas

CREATE TABLE stats (
    countrycode character(3) PRIMARY KEY,
    cant_lenguas integer NOT NULL,
    pop_urbana integer NOT NULL,
    CONSTRAINT fk_countrycode
        FOREIGN KEY(countrycode) 
	        REFERENCES country(code)
);

INSERT INTO stats (countrycode, cant_lenguas, pop_urbana)
SELECT c.code contrycode, count_languages.count cant_lenguas, population.sum_population pop_urbana
FROM country c
INNER JOIN (
    SELECT countrycode, count(*) count FROM countrylanguage GROUP BY countrycode
) count_languages
ON c.code = count_languages.countrycode
INNER JOIN (
    SELECT countrycode, SUM(population) sum_population FROM city GROUP BY countrycode
) population
ON c.code = population.countrycode;

-- 3.4 
-- El archivo "top-1m.csv" contiene la informacion ordenada del 1er. millon de sitios de internet con mayor traco (la
-- medicion corresponde al a~no 2012). La estructura del archivo es la siguiente:
-- Cada lnea es de la forma: < nro: de orden >;< dominio >
-- Cada dominio es de la forma: XXXXX.YYY.ZZ
-- Se pide crear la siguiente tabla
-- Nombre: sitio
-- Campos:
--  id: int (es el numero de orden que aparece en cada lnea de la archivo)/primary key
--  entidad: varchar (1ra. parte del dominio: hasta el 1er. punto)
--  tipo entidad: varchar (2da. parte del dominio)
--  pas: varchar (3ra. parte dela dominio)
--  countrycode: foreign key a country.code

CREATE TABLE sitio (
    id integer PRIMARY KEY,
    entidad text NOT NULL,
    tipo_entidad text NOT NULL,
    pais  text,
    countrycode character(3),
    CONSTRAINT fk_countrycode
        FOREIGN KEY(countrycode) 
	        REFERENCES country(code)
);

CREATE TABLE sitio2 (
    id integer PRIMARY KEY,
    entidad text,
    tipo_entidad text,
    pais  text,
    countrycode character(3),
    CONSTRAINT fk_countrycode
        FOREIGN KEY(countrycode) 
	        REFERENCES country(code)
);


-- 3.5. Ejercicio 5

SELECT *
FROM sitio s1, sitio s2
WHERE s1.countrycode = s2.countrycode
AND s1.entidad LIKE 'a%' and s2.entidad LIKE 'b%'
LIMIT 100 

<<<<<<< HEAD
-- Se llama dos veces a la tabla sitio, una con alias s1 y la otra con alias s2 
-- en el select se repiten las columnas), al alias s1 se le agrega una condicion de que las
-- entidades empiecen con "a" y s2 con "b", luego se hace un producto cartesiano donde cada
-- registro de s1 se deben corresponder a todas las filas de s2, y luego sucede a viceversa

-- PRUEBAS DE INDICES

-- SIN INDICE

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


-- CON INDICE BTREE

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



-- CON INDICE GIN

--  Limit  (cost=0.00..4.14 rows=100 width=50) (actual time=0.147..80.617 rows=100 loops=1)
--    ->  Nested Loop  (cost=0.00..53530877.55 rows=1291943472 width=50) (actual time=0.146..80.590 rows=100 loops=1)
--          Join Filter: (s1.countrycode = s2.countrycode)
--          Rows Removed by Join Filter: 35435
--          ->  Seq Scan on sitio2 s2  (cost=0.00..19531.00 rows=50470 width=25) (actual time=0.026..0.027 rows=1 loops=1)
--                Filter: (entidad ~~ 'b%'::text)
--                Rows Removed by Filter: 24
--          ->  Materialize  (cost=0.00..19884.29 rows=70658 width=25) (actual time=0.013..76.065 rows=35535 loops=1)
--                ->  Seq Scan on sitio2 s1  (cost=0.00..19531.00 rows=70658 width=25) (actual time=0.006..68.815 rows=35535 loops=1)
--                      Filter: (entidad ~~ 'a%'::text)
--                      Rows Removed by Filter: 483000
--  Planning Time: 0.594 ms
--  Execution Time: 81.295 ms
-- (13 rows)
=======
-- Trae 
>>>>>>> 56e707c43c410b29964330a826c011c4ebb66053
