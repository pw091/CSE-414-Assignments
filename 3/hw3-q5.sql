SELECT f.origin_city as city
FROM flights f
GROUP BY f.origin_city
HAVING f.origin_city!='Seattle WA'
EXCEPT (
    SELECT f2.dest_city as city
    FROM flights f1
        INNER JOIN flights f2 ON f1.dest_city=f2.origin_city
    WHERE f1.origin_city='Seattle WA'
        AND f2.dest_city!='Seattle WA'
    GROUP BY f2.dest_city
)
ORDER BY f.origin_city ASC;

--4 rows affected
--Total execution time: 00:00:01.967
/*
city
Devils Lake ND
Hattiesburg/Laurel MS
St. Augustine FL
Victoria TX
*/
