-- This file dictates the structure of the tables for 
-- V1.2 of dzbnb

BEGIN;

DROP TABLE IF EXISTS viewlog, reviews,reservations, properties, users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(32) NOT NULL, 
    email VARCHAR(128) NOT NULL UNIQUE, --Need validation in Python.
    password VARCHAR(32) NOT NULL, 
    hidden BOOLEAN DEFAULT FALSE, 
    admin BOOLEAN DEFAULT FALSE, 
    reg_time TIMESTAMP NOT NULL DEFAULT now(), 
    last_login TIMESTAMP NOT NULL DEFAULT now(), 
    login_count INT NOT NULL DEFAULT 0,
    CHECK (login_count >= 0),
    CHECK (last_login >= reg_time)
);

CREATE TABLE properties (
    id serial primary key, 
    owner INT NOT NULL REFERENCES USERS(ID), 
    name VARCHAR(128) NOT NULL,
    hidden BOOLEAN DEFAULT FALSE, 
    creation_date TIMESTAMP NOT NULL, 
    size REAL, 
    price REAL, 
    description VARCHAR(4096),
    CHECK (size > 0),
    CHECK (price >= 0)
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY, 
    property INT NOT NULL REFERENCES PROPERTIES(ID), 
    renter INT NOT NULL REFERENCES USERS(ID), 
    start_date DATE, 
    end_date DATE,
    approved BOOLEAN DEFAULT FALSE,
    CHECK (end_date > start_date)
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    reviewer INT NOT NULL REFERENCES USERS(ID), 
    property INT NOT NULL REFERENCES PROPERTIES(ID), 
    hidden BOOLEAN DEFAULT FALSE, 
    rating INT, 
    comment VARCHAR(4096), 
    review_time TIMESTAMP NOT NULL DEFAULT now(),
    CHECK ((rating >= 1) AND (rating <= 5))
);

CREATE TABLE viewlog (
    id SERIAL PRIMARY KEY, 
    property INT NOT NULL REFERENCES PROPERTIES(ID), 
    viewer INT NOT NULL REFERENCES USERS(ID), 
    viewtime TIMESTAMP NOT NULL DEFAULT now()
);
COMMIT;
