SELECT c.name as carrier
FROM carriers c
    INNER JOIN flights f
        ON f.carrier_id = c.cid
WHERE f.origin_city='Seattle WA'
    AND f.dest_city='San Francisco CA'
GROUP BY c.name
ORDER BY c.name ASC;

--4 rows affected
--Total execution time: 00:00:00.039
/*
carrier
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America
*/
