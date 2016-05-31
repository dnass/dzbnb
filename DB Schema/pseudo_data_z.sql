BEGIN;

--TRUNCATE users CASCADE; -- comment out this line before sending to Dan.

-- remember how many rows to start with and will need display the changes after everything
DROP TABLE IF EXISTS temp_records;
CREATE TABLE temp_records (users_count INT, properties_count INT, reservations_count INT, reviews_count INT, views_count INT);
INSERT INTO temp_records (users_count, properties_count, reservations_count, reviews_count, views_count)
    SELECT
        (SELECT count(*) FROM users),
        (SELECT count(*) FROM properties),
        (SELECT count(*) FROM reservations),
        (SELECT count(*) FROM reviews),
        (SELECT count(*) FROM viewlog);

-- User #1 and 3 of his properties.
INSERT INTO users (name,email, password, reg_time, last_login)
    VALUES ('Michael Jackson', 'mcsuperstar@fuckup.com', md5(random()::text), now(), now());

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'Racist villa with nested bathrooms', now(), 1000.5, 2999.99, 'The best villa for ethinic and kinky couples!');

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'Studio without windows', now(), 30.8, 25.80, 'The best apartment for lonely single depressed nerd.');

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'Finally a nice place', now(), 500, 9.99, 'The cheapest place ever!!');

-- User #2 and 1 unapproved reservation of User #1's last property
INSERT INTO users (name,email, password, reg_time, last_login)
    VALUES ('Jimmy Kimmel', 'james_K@heygirl.com', md5(random()::text), now(), now());

INSERT INTO reservations (property, renter, start_date, end_date)
    VALUES (currval('properties_id_seq'), currval('users_id_seq'), '2015-01-01', '2015-01-05');

-- User #3 and 2 properties
INSERT INTO users (name,email, password, reg_time, last_login)
    VALUES ('Ellen D', 'cutelittlewoman@america.com', md5(random()::text), now(), now());

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'Bright apartment with candles', now(), 240.5, 299.00, 'What are you talking about? I have no idea.');

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'Large loft without bathroom', now(), 3000.8, 2556.60, 'The most stupid people will rent this place. Where the fuck do you want to pee?');

-- User #4 and 1 approved reservation of User #3's, 0 property, a comment to User #3's.
INSERT INTO users (name,email, password, reg_time, last_login)
    VALUES ('Johnson Palmer', 'johnsonsexyhunk@cccciiiiiaaaa.com', md5(random()::text), now(), now());

INSERT INTO reservations (property, renter, start_date, end_date, approved)
    VALUES (currval('properties_id_seq'), currval('users_id_seq'), '2015-01-01', '2015-01-05', TRUE);

INSERT INTO reviews (reviewer, property, rating, comment)
    VALUES (currval('users_id_seq'), currval('properties_id_seq'), 5, 'Best place ever!');

-- User #5, 1 approved reservation User #3's, 1 property, 1 comment to User #4's

INSERT INTO users (name,email, password, reg_time, last_login)
    VALUES ('Chen Shabi', 'chensilly@huhuhahi.com', md5(random()::text), now(), now());

INSERT INTO reservations (property, renter, start_date, end_date, approved)
    VALUES (currval('properties_id_seq'), currval('users_id_seq'), '2016-05-05', '2016-07-05', TRUE);

INSERT INTO reviews (reviewer, property, rating, comment)
    VALUES (currval('users_id_seq'), currval('properties_id_seq'), 1, 'Bad Bad Bad');

INSERT INTO properties (owner, name, creation_date, size, price, description)
    VALUES (currval('users_id_seq'), 'CrossFit box for rent', now(), 245.7, 15.8, 'Who would want to sleep on dirty sweaty gym floor mats?');

-- Add 1,000 reviews and remove the reviews that are added by the property owners themselves.
DO
$do$
BEGIN
FOR i in 1..1000 LOOP
    INSERT INTO reviews (reviewer, property, rating)
        SELECT 
            (SELECT id FROM users ORDER BY random() limit 1), 
            (SELECT id FROM properties ORDER BY random() limit 1), 
            floor(random()*5)+1;
END LOOP;
END
$do$;
DELETE FROM reviews
    WHERE reviewer = (SELECT owner FROM properties WHERE properties.id = reviews.property);

-- Add 50,000 random records into viewlog and remove the views by the property owners themselves.
DO
$do$
BEGIN
FOR i in 1..50000 LOOP
    INSERT INTO viewlog (property, viewer, viewtime)
        SELECT
            (SELECT id FROM properties ORDER BY random() limit 1),
            (SELECT id FROM users ORDER BY random() limit 1), 
            (SELECT TIMESTAMP '2016-01-01 00:00:00' + random() * (now() - TIMESTAMP '2016-01-01 00:00:00'));
END LOOP;
END
$do$;

DELETE FROM viewlog WHERE viewer = (SELECT owner FROM properties WHERE properties.id = viewlog.property);

INSERT INTO temp_records (users_count, properties_count, reservations_count, reviews_count, views_count)
    SELECT
        (SELECT count(*) as users_count from users),
        (SELECT count(*) as properties_count from properties),
        (SELECT count(*) as reservations_count from reservations),
        (SELECT count(*) as reviews_count from reviews),
        (SELECT count(*) as views_count from viewlog);

SELECT * FROM temp_records;
DROP TABLE IF EXISTS temp_records;

COMMIT;
