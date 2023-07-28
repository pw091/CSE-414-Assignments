SELECT w.day_of_week, avg(f.arrival_delay) as delay
FROM flights f
    INNER JOIN weekdays w ON f.day_of_week_id=w.did
GROUP BY w.day_of_week
ORDER BY delay DESC
LIMIT 1;
--1 row