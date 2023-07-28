SELECT DISTINCT c.name
FROM flights f1
    INNER JOIN carriers c ON f1.carrier_id=c.cid
GROUP BY c.name, f1.day_of_month, f1.month_id
HAVING count(*)>1000;
--12 rows