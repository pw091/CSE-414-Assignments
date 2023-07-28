SELECT c.name, avg(f.canceled)*100 as percentage
FROM flights f
    INNER JOIN carriers c ON f.carrier_id=c.cid
WHERE f.origin_city='Seattle WA'
GROUP BY c.name
HAVING percentage > 0.5;
--6 rows