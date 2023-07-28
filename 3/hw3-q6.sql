SELECT c.name as carrier
FROM carriers c
WHERE c.name IN (
    SELECT c2.name
    FROM carriers c2
        INNER JOIN flights f
            ON c2.cid=f.carrier_id
    WHERE f.origin_city='Seattle WA'
        AND f.dest_city='San Francisco CA'
    GROUP BY c2.name
    )
ORDER BY c.name ASC;

--4 rows affected
--Total execution time: 00:00:00.050
/*
carrier
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America
*/