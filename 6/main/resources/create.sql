CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) NOT NULL
        REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Appointments (
    Appointment_id varchar(255),
    Time date,
    Caregiver_uname varchar(255) NOT NULL
        REFERENCES Caregivers,
    Patient_uname varchar(255) NOT NULL
        REFERENCES Patients,
    Vaccine_name varchar(255) NOT NULL
        REFERENCES Vaccines,
    PRIMARY KEY (Appointment_id)
);