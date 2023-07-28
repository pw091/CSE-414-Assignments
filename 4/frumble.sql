--Q1
CREATE TABLE Frumble (
    name varchar(100),
    discount varchar(100),
    month varchar(100),
    price int
);

--Q2 (summary at bottom)
--SIMPLE
--NAME IMPLICATIONS
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.discount != f2.discount);
--3286, !=> discount

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.month != f2.month);
--4620, !=> month

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.price != f2.price);
--0, => price

--DISCOUNT IMPLICATIONS
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.name != f2.name);
--61398, !=> name

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.month != f2.month);
--48032, !=> month

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.price != f2.price);
--55170, !=> price

--MONTH IMPLICATIONS
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.month = f2.month)
AND (f1.name != f2.name);
--14700, !=> name

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.month = f2.month)
AND (f1.discount != f2.discount);
--0, => discount

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.month = f2.month)
AND (f1.price != f2.price);
--13208, !=> price

--PRICE IMPLICATIONS
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.price = f2.price)
AND (f1.name != f2.name);
--17906, !=> name

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.price = f2.price)
AND (f1.discount != f2.discount);
--14964, !=> discount

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.price = f2.price)
AND (f1.month != f2.month);
--21034, !=> month

/*
Thus, the simple dependencies are:
Name->Price
Month->Discount
*/

--2-dependencies
--Name,Discount
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.discount = f2.discount)
AND (f1.month != f2.month);
--1334

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.discount = f2.discount)
AND (f1.price != f2.price);
--0

--Name,Month
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.month = f2.month)
AND (f1.discount != f2.discount);
--0

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.month = f2.month)
AND (f1.price != f2.price);
--0

--Name,Price
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.price = f2.price)
AND (f1.discount != f2.discount);
--3286

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.price = f2.price)
AND (f1.month != f2.month);
--4620

--Discount,Month
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.month = f2.month)
AND (f1.name != f2.name);
--14700

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.month = f2.month)
AND (f1.price != f2.price);
--13208

--Discount,Price
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.price = f2.price)
AND (f1.name != f2.name);
--6228

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.price = f2.price)
AND (f1.month != f2.month);
--6070

--Month,Price
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.month = f2.month)
AND (f1.price = f2.price)
AND (f1.name != f2.name);
--1492

SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.month = f2.month)
AND (f1.price = f2.price)
AND (f1.discount != f2.discount);
--0

/*
Pair dependencies:
(Name, Discount) -> Price
(Name, Month) -> Discount
(Name, Month) -> Price
(Month, Price) -> Discount
*/

--3-dependencies
--Name,Discount,Month
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.discount = f2.discount)
AND (f1.month = f2.month)
AND (f1.price != f2.price);
--0

--Name,Discount,Price
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.name = f2.name)
AND (f1.discount = f2.discount)
AND (f1.price = f2.price)
AND (f1.month != f2.month);
--1334

--Discount,Month,Price
SELECT count(*)
FROM Frumble f1, Frumble f2
WHERE (f1.discount = f2.discount)
AND (f1.month = f2.month)
AND (f1.price = f2.price)
AND (f1.name != f2.name);
--1492

/*
Triple dependencies:
(Name,Discount,Month) -> Price
*/

/*
All unique dependencies:
Name->Price
Month->Discount
(Name, Discount) -> Price
(Name, Month) -> Discount
(Name, Month) -> Price
(Month, Price) -> Discount
(Name,Discount,Month) -> Price
*/

--Q3
CREATE TABLE NamePrice (
    name varchar(100),
    price int,
    PRIMARY KEY (name)
);

CREATE TABLE DiscountMonth (
    discount varchar(100),
    month varchar(100),
    PRIMARY KEY (month)
);

CREATE Table NameMonth (
    name varchar(100),
    month varchar(100),
    PRIMARY KEY (name, month),
    FOREIGN KEY (name) REFERENCES NamePrice(name),
    FOREIGN KEY (month) REFERENCES DiscountMonth(month)
);

--Q4
INSERT INTO NamePrice (name, price)
SELECT DISTINCT f.name, f.price
FROM Frumble f;

SELECT count(*)
FROM NamePrice;
--36

INSERT INTO DiscountMonth (discount, month)
SELECT DISTINCT f.discount, f.month
FROM Frumble f;

SELECT count(*)
FROM DiscountMonth;
--12

INSERT INTO NameMonth (name, month)
SELECT DISTINCT f.name, f.month
FROM Frumble f;

SELECT count(*)
FROM NameMonth;
--426