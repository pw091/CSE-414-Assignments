SELECT f.origin_city as city
FROM flights f
WHERE f.canceled=0
GROUP BY f.origin_city
HAVING max(f.actual_time)<3*60
ORDER BY f.origin_city ASC;

--109 rows affected
--Total execution time: 00:00:05.498
/*
city
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA
*/