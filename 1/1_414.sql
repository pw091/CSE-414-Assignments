--Q2
CREATE TABLE Edges (
    Source int,
    Destination int
);

INSERT INTO Edges
(Source, Destination)
VALUES (10,5),(6,25),(1,3),(4,4);

SELECT *
FROM Edges;

SELECT Source
FROM Edges;

SELECT *
FROM Edges
WHERE Source>Destination;

INSERT INTO Edges
(Source, Destination)
VALUES ('-1','2000');
--There is no error; this does not match
--my expectations from the relational model.
--In theory, types are static and strictly enforced,
--yet this DBMS implementation allows non-integer
--values for integer attributes.

--Q3
CREATE TABLE MyRestaurants (
    Name varchar,
    Food varchar,
    Distance int,
    Visit_date varchar,
    You_like int
);

--Q4
INSERT INTO MyRestaurants
(Name, Food, Distance, Visit_date, You_like)
VALUES ('Rest. A', 'Apples', 5, '2000-01-01', 0);

INSERT INTO MyRestaurants
(Name, Food, Distance, Visit_date, You_like)
VALUES ('Rest. B', 'Bananas', 10, '2000-01-02', 0);

INSERT INTO MyRestaurants
(Name, Food, Distance, Visit_date, You_like)
VALUES ('Rest. C', 'Carrots', 15, '2000-01-03', 1);

INSERT INTO MyRestaurants
(Name, Food, Distance, Visit_date, You_like)
VALUES ('Rest. D', 'Donuts', 20, '2000-01-04', 1);

INSERT INTO MyRestaurants
(Name, Food, Distance, Visit_date, You_like)
VALUES ('Rest. E', 'Eggs', 25, '2000-01-05', NULL);

--Q5
.headers on
.mode csv
SELECT * FROM MyRestaurants;

.mode list
SELECT * FROM MyRestaurants;

.mode column
.width 15 15 15 15 15
SELECT * FROM MyRestaurants;

.headers off
.mode csv
SELECT * FROM MyRestaurants;

.mode list
SELECT * FROM MyRestaurants;

.mode column
.width 15 15 15 15 15
SELECT * FROM MyRestaurants;

--Q6
SELECT Name, Distance
FROM MyRestaurants
WHERE Distance<=20
ORDER BY Name ASC;

--Q7
SELECT *
FROM MyRestaurants
WHERE You_like=1 AND date('now','-3 month')>date(Visit_date);

--Q8
SELECT *
FROM MyRestaurants
WHERE Distance<=10;