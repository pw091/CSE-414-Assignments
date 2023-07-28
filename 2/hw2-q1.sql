SELECT flight_num
FROM flights f
    INNER JOIN carriers c ON f.carrier_id=c.cid
    INNER JOIN weekdays w ON f.day_of_week_id=w.did
WHERE origin_city='Seattle WA'
    AND dest_city='Boston MA'
    AND name='Alaska Airlines Inc.'
    AND day_of_week='Monday'
GROUP BY flight_num;
--3 rows