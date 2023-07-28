SELECT c.name, 
    f1.flight_num as f1_flight_num, f1.origin_city as f1_origin_city, f1.dest_city as f1_dest_city, f1.actual_time as f1_actual_time,
    f2.flight_num as f2_flight_num, f2.origin_city as f2_origin_city, f2.dest_city as f2_dest_city, f2.actual_time as f2_actual_time,
    f1.actual_time+f2.actual_time as actual_time
FROM flights f1
    INNER JOIN flights f2 ON f1.dest_city=f2.origin_city
    INNER JOIN carriers c ON f1.carrier_id=c.cid
    INNER JOIN months m ON f1.month_id=m.mid
WHERE f1.origin_city='Seattle WA'
    AND f2.dest_city='Boston MA'
    AND f1.carrier_id=f2.carrier_id
    AND m.month='July'
    AND f1.day_of_month=15
    AND f2.day_of_month=15
    AND f1.actual_time+f2.actual_time<7*60
GROUP BY f1.flight_num, f2.flight_num;
--1472 rows