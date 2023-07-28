SELECT c.name as carrier, max(price) as max_price
FROM flights f
    INNER JOIN carriers c ON f.carrier_id=c.cid
WHERE (f.origin_city='Seattle WA' and f.dest_city='New York NY')
    OR (f.origin_city='New York NY' and f.dest_city='Seattle WA')
GROUP BY c.name;
--3 rows