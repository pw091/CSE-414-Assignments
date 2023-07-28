SELECT c.name, sum(f.departure_delay) as delay
FROM flights f
    INNER JOIN carriers c ON f.carrier_id=c.cid
GROUP BY c.name;
--22 rows