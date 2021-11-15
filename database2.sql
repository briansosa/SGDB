-- 3.1.1
-- CREATE DATABASE world;

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

SELECT c.name, countrylanguage.sum_population, city.name city_name, (city.population * 100 / countrylanguage.sum_population) percent_population
FROM country c
INNER JOIN (
    SELECT countrycode, SUM(population) sum_population FROM city GROUP BY countrycode
) countrylanguage
ON c.code = countrylanguage.countrycode
INNER JOIN city ON c.code = city.countrycode
ORDER BY c.name;