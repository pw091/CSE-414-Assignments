SELECT f2.dest_city as city
FROM flights f1
    INNER JOIN flights f2 ON f1.dest_city=f2.origin_city
WHERE f1.origin_city='Seattle WA'
    AND f2.dest_city!='Seattle WA'
GROUP BY f2.dest_city
EXCEPT
    (
    SELECT f1.dest_city as city
    FROM flights f1
    WHERE f1.origin_city='Seattle WA'
    GROUP BY f1.dest_city
    )
ORDER BY f2.dest_city ASC;

--256 rows affected
--Total execution time: 00:00:05.328
/*
city
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME
*/
