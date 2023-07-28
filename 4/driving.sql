--Note: This implementation is for SQLite. 'PRAGMA foreign_keys=ON;' is needed when using the DB.
--I did not explicitly include this as the question did not ask for it.
--a)
CREATE TABLE InsuranceCo(
    name varchar(100),
    phone int,
    PRIMARY KEY (name)
);

CREATE Table Insures(
    maxLiability float,
    name varchar(100),
    licensePlate varchar(100),
    PRIMARY KEY (licensePlate),
    FOREIGN KEY (name) REFERENCES InsuranceCo(name) --insuranceCo "insures"
);

CREATE TABLE Person(
    ssn int,
    name varchar(100),
    PRIMARY KEY (ssn)
);

CREATE TABLE Driver(
    ssn int,
    driverID int,
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES Person(ssn) --is a person
);

CREATE TABLE NonProfessionalDriver(
    ssn int,
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES Driver(ssn) --is a driver
);

CREATE TABLE ProfessionalDriver(
    ssn int,
    medicalHistory varchar(100),
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES Driver(ssn) --is a driver
);

CREATE TABLE Vehicle(
    licensePlate varchar(100),
    year int,
    ssn int,
    PRIMARY KEY (licensePlate),
    FOREIGN KEY (licensePlate) REFERENCES Insures(licensePlate), --insured by "insures"
    FOREIGN KEY (ssn) REFERENCES Person(ssn) --person owns vehicle
);

CREATE TABLE Truck(
    licensePlate varchar(100),
    capacity int,
    ssn int,
    PRIMARY KEY (licensePlate),
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate), --is a vehicle
    FOREIGN KEY (ssn) REFERENCES ProfessionalDriver(ssn) --professional driver operates truck
);

CREATE TABLE Car(
    licensePlate varchar(100),
    make varchar(100),
    PRIMARY KEY (licensePlate),
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate) --is a vehicle
);

CREATE TABLE Drives(
    licensePlate varchar(100),
    ssn int,
    PRIMARY KEY (licensePlate, ssn),
    FOREIGN KEY (licensePlate) REFERENCES Car(licensePlate),
    FOREIGN KEY (ssn) REFERENCES NonProfessionalDriver(ssn)
);

/*
b) A separate table (Insures) with a foreign key referencing InsuranceCo (and implicitly, the foreign in vehicle
referencing Insures). This allows me to encode both the one-to-many relationship and maxLiability as an
attribute of the relationship itself instead of violating the model by placing maxLiability as an attribute of
another table in which it is not specified as an attribute.

c) 'Drives' is a many-to-many relationship, while 'Operates' is a one-to-many. 'Drives' has its own table to
track references in both direction (Car and NonProfessionalDriver) with foreign keys, whereas 'Operates' is 
a foreign key of 'Truck' since all rows can be attributed to a single row in 'ProfessionalDriver'.