begin;
insert into users (name, email, password, admin, reg_time, last_login, login_count)
  values ('Dang Gnass', 'dangiel@gmail.dang', 'fbade9e36a3f36d3d676c1b808451dd7', true, current_timestamp, current_timestamp, 7);

insert into users (name, email, password, hidden, reg_time, last_login, login_count)
  values ('Dzhengyu Rend', 'big_z_unit@emailforchinesepeople???.com', 'fbadw9e36a3f36d3d676c1b808451dd7', true, current_timestamp, '2017-04-13', 2);

insert into users (name, email, password, admin, hidden, reg_time, last_login)
  values ('Hun Sen', 'hunsend@cambodia.biz', 'fbedw9e36a3f36d3d676c1b808451dd7', true, true, '1995-01-01', '1999-01-11');

insert into users (name, email, password, reg_time, last_login)
  values ('Svetlana Ng', 'svng@russia.russia.russia.russia', 'zzzzzzzzzzzzz', '1950-11-13', '1951-12-21');

insert into users (name, email, password, reg_time, last_login, login_count)
  values ('Lance Boyle', 'itsapun@fuccccckkkkkk.info', 'funny name for a dermatologist', current_timestamp, '2016-06-29', 1);

insert into properties (owner, name, creation_date, size, price, description)
  values ((select id from users where name = 'Hun Sen'), 'My house', '2004-03-06', 300, 5000, 'nice little place on norodom');

insert into properties (owner, name, creation_date, size, price, description)
  values ((select id from users where name = 'Hun Sen'), 'My other house', '2008-08-10', 500, 10000, 'this one is in sihanoukville');

insert into properties (owner, name, creation_date, size, price, description)
  values ((select id from users where name = 'Dang Gnass'), 'Trashcan', current_timestamp, 1, 0.01, 'so sad');

  insert into properties (owner, name, creation_date, size, price, description)
    values ((select id from users where name = 'Dzhengyu Rend'), 'Apartment', '2011-01-11', 120, 500, 'really the only reasonable option');

insert into properties (owner, name, hidden, creation_date, size, price, description)
  values ((select id from users where name = 'Svetlana Ng'), 'WHATEVER', true, '1901-01-01', 10000.00001, 5000000, 'hidden 4 a reason');

insert into reservations (property, renter, start_date, end_date, approved)
  values ((select id from properties where name = 'My house'), (select id from users where name = 'Dang Gnass'), '2016-05-11', '2016-06-11', true);

insert into reservations (property, renter, start_date, end_date)
  values ((select id from properties where name = 'My house'), (select id from users where name = 'Dzhengyu Rend'), '2016-05-22', '2016-06-22');

insert into reservations (property, renter, start_date, end_date, approved)
  values ((select id from properties where name = 'My other house'), (select id from users where name = 'Dang Gnass'), '2016-05-11', '2016-06-29', true);

insert into reservations (property, renter, start_date, end_date, approved)
  values ((select id from properties where name = 'Trashcan'), (select id from users where name = 'Hun Sen'), '1901-01-01', '2100-12-31', true);

insert into reservations (property, renter, start_date, end_date)
  values ((select id from properties where name = 'WHATEVER'), (select id from users where name = 'Svetlana Ng'), '1995-04-03', '1998-12-17');

insert into reviews (reviewer, property, hidden, rating, comment, review_time)
  values ((select id from users where name = 'Dang Gnass'), (select id from properties where name = 'My other house'), true, 4, 'nice place', '2016-05-11');

insert into reviews (reviewer, property, rating, comment)
  values ((select id from users where name = 'Dang Gnass'), (select id from properties where name = 'My house'), 1, 'terrible');

insert into reviews (reviewer, property, rating, comment, review_time)
  values ((select id from users where name = 'Lance Boyle'), (select id from properties where name = 'WHATEVER'), 2, 'WHATEVER YO', '1911-12-13');

insert into reviews (reviewer, property, rating, comment)
  values ((select id from users where name = 'Hun Sen'), (select id from properties where name = 'Trashcan'), 5, 'i <3 trash');

insert into reviews (reviewer, property, hidden, rating, comment)
  values ((select id from users where name = 'Dzhengyu Rend'), (select id from properties where name = 'Apartment'), true, 5, 'I AM TRAPPED INSIDE A DATABASE OH NO');

insert into viewlog (property, viewer, viewtime)
  values ((select id from properties where name = 'My house'), (select id from users where name = 'Dang Gnass'), '2015-08-11');

insert into viewlog (property, viewer)
  values ((select id from properties where name = 'My house'), (select id from users where name = 'Dzhengyu Rend'));

insert into viewlog (property, viewer)
  values ((select id from properties where name = 'Trashcan'), (select id from users where name = 'Hun Sen'));

insert into viewlog (property, viewer, viewtime)
  values ((select id from properties where name = 'My other house'), (select id from users where name = 'Svetlana Ng'), '2013-11-11');

insert into viewlog (property, viewer)
  values ((select id from properties where name = 'WHATEVER'), (select id from users where name = 'Lance Boyle'));
commit;