SELECT f.origin_city,
    avg(CASE WHEN (f.actual_time<3*60 OR f.actual_time=NULL) THEN 100.0 ELSE 0.0 END) as 'percentage'
FROM flights f
WHERE f.canceled = 0
GROUP BY f.origin_city
ORDER BY 'percentage' ASC, f.origin_city ASC;

--327 rows affected
--Total execution time: 00:00:05.253
/*
origin_city percentage
Guam TT	0.000000
Pago Pago TT	0.000000
Aguadilla PR	28.897338
Anchorage AK	31.812080
San Juan PR	33.660531
Charlotte Amalie VI	39.558823
Ponce PR	40.983606
Fairbanks AK	50.116550
Kahului HI	53.514471
Honolulu HI	54.739028
San Francisco CA	55.828864
Los Angeles CA	56.080890
Seattle WA	57.609387
Long Beach CA	62.176439
New York NY	62.371834
Kona HI	63.160792
Las Vegas NV	64.920256
Christiansted VI	65.100671
Newark NJ	65.849971
Plattsburgh NY	66.666666
*/
