-- DROPING TABLES
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS petitions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS offices;
DROP TABLE IF EXISTS parties;


-- CREATING TABLES
CREATE TABLE offices(
    id serial primary key, office_name varchar(20), office_type varchar(20)
    );


-- this table has the basic 
CREATE TABLE parties (
    id serial primary key, party_name varchar(30), party_hq_address varchar(20), party_logo_url text
);


CREATE TABLE users(
    -- id serial primary key, username varchar(20), email varchar(30) unique, password varchar(100), office_id integer references offices(id),
    id serial primary key, first_name varchar(20), last_name varchar(20), other_name varchar(20), email varchar(50) UNIQUE NOT NULL, 
    password varchar(100) NOT NULL, phone_number varchar(20), passport_url varchar(100), is_politician boolean, is_admin boolean, 
    political_party integer REFERENCES parties(id), office_interested integer REFERENCES offices(id)
    );


-- votes table that has [ID, voting user, voted user('politician'), office_id ('position being vied for')]
CREATE TABLE votes (
    id serial primary key, created_on date NOT NULL DEFAULT CURRENT_DATE, created_by integer references users(id), office integer references offices(id),
    voted_for integer references users(id)
);

-- holding all the petitions after the elections are office
create table petitions (
    id serial primary key, created_on date NOT NULL DEFAULT CURRENT_DATE, create_by integer references users(id), office integer references offices(id),
     body text
     );

