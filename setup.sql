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
    id serial primary key, first_name varchar(20), last_name varchar(20), other_name varchar(20), email varchar(50), phone_number varchar(20),
    passport_url varchar(100), is_politician boolean, is_admin boolean, political_party integer REFERENCES parties(id), 
    office_interested integer REFERENCES offices(id)
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


-- INSERTING DUMMY DATA TO THE TABLES 
-- CREATE NEW DUMMY OFFICES

-- if you would like to test out the dummy data, uncomment from here to the place ending with the exclamation marks
-- START !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! START 
-- INSERT INTO offices (office_name, office_type) VALUES 
-- ('presidencial', 'legislative'),
-- ('headboy', 'school');

-- -- CREATING NEW DUMMY POLITICAL PARTIES
-- INSERT INTO parties ( party_name, party_hq_address, party_logo_url ) VALUES 
-- ('Democrats', 'New york', 'democrats logo url'),
-- ('Republicans', 'Washington DC', 'repub logo url');

-- -- CREATE DUMMY POLITICO USERS WHO ARE NOT POLITICIANS
-- INSERT INTO users (first_name, last_name, other_name, email, phone_number, passport_url) VALUES 
-- ('voter1_first', 'voter1_last', 'voter1_other', 'voter1@voter1.com', '07102737457', 'voter1_passport'),
-- ('voter2_first', 'voter2_last', 'voter2_other', 'voter2@voter2.com', '07140737457', 'voter2_passport'),
-- ('voter3_first', 'voter3_last', 'voter3_other', 'voter3@voter3.com', '07146737457', 'voter3_passport'),
-- ('voter4_first', 'voter4_last', 'voter4_other', 'voter4@voter4.com', '07108737457', 'voter4_passport'),
-- ('voter5_first', 'voter5_last', 'voter5_other', 'voter1@voter5.com', '07164737457', 'voter5_passport'),
-- ('voter6_first', 'voter6_last', 'voter6_other', 'voter1@voter6.com', '07180737457', 'voter6_passport'),
-- ('voter7_first', 'voter7_last', 'voter7_other', 'voter1@voter7.com', '07112737457', 'voter7_passport'),
-- ('voter8_first', 'voter8_last', 'voter8_other', 'voter1@voter8.com', '07191737457', 'voter8_passport'),
-- ('voter9_first', 'voter9_last', 'voter9_other', 'voter1@voter9.com', '07180737457', 'voter9_passport'),
-- ('voter10_first', 'voter10_last', 'voter10_other', 'voter1@voter10.com', '07562737457', 'voter10_passport'),
-- ('voter11_first', 'voter11_last', 'voter11_other', 'voter1@voter11.com', '07652737457', 'voter11_passport'),
-- ('voter12_first', 'voter12_last', 'voter12_other', 'voter1@voter12.com', '07832737457', 'voter12_passport'),
-- ('voter13_first', 'voter13_last', 'voter13_other', 'voter1@voter13.com', '07122737457', 'voter13_passport')
-- ;

-- -- CREATE DUMMY USERS WHO ARE  POLITICIANS 
-- INSERT INTO users(first_name, last_name, other_name, email, phone_number, passport_url, is_politician, political_party, office_interested) VALUES 
-- -- two political candidates both vying for the presidential seat
-- ('politician1_first', 'politician1_last', 'politician1_other', 'politician1@poltician1.com', '07034566723', 'politican1_passport', true, 1, 1),
-- ('politician2_first', 'politician2_last', 'politician2_other', 'politician2@poltician2.com', '07078566723', 'politican2_passport', true, 2, 1);

-- -- two politicians both vying to be the headboy (LOL)
-- INSERT INTO users(first_name, last_name, other_name, email, phone_number, passport_url, is_politician, political_party, office_interested) VALUES 
-- ('headboy1_first', 'headboy1_last', 'headboy1_other', 'headboy1@headboy1.com', '0717273745', 'headboy1_passport', true, 1, 2),
-- ('headboy2_first', 'headboy2_last', 'headboy2_other', 'headboy2@headboy2.com', '0717273745', 'headboy2_passport', true, 2, 2);


-- -- PRESIDENCY VOTES
-- -- the first 10 voters will vote for politician1 and the last last three will vote for politican2
-- INSERT INTO votes(created_by, office, voted_for) VALUES 
-- (1, 1, 14),
-- (2, 1, 14),
-- (3, 1, 14),
-- (4, 1, 14),
-- (5, 1, 14),
-- (6, 1, 14),
-- (7, 1, 14),
-- (8, 1, 14),
-- (9, 1, 14),
-- (10, 1, 14),
-- (11, 1, 15),
-- (12, 1, 15),
-- (13, 1, 15);

-- -- HEADBOY VOTES
-- -- the first 8 will vote for headboy1 and the last 5 will vote for headboy2
-- INSERT INTO votes(created_by, office, voted_for) VALUES 
-- (1, 2, 16),
-- (2, 2, 16),
-- (3, 2, 16),
-- (4, 2, 16),
-- (5, 2, 16),
-- (6, 2, 16),
-- (7, 2, 16),
-- (8, 2, 16),
-- (9, 2, 17),
-- (10, 2, 17),
-- (11, 2, 17),
-- (12, 2, 17),
-- (13, 2, 17);

-- -- GET THE RESULTS FOR THE PRESIDENCY
-- SELECT users.id, users.first_name, count(votes.voted_for) as number_of_votes from users 
-- LEFT JOIN votes 
-- ON (votes.voted_for=users.id)
-- WHERE (users.is_politician=true) AND (users.office_interested=1)
-- group by users.id;

-- -- GET THE RESULTS FOR BEING THE HEADBOY
-- SELECT users.id, users.first_name, count(votes.voted_for) as number_of_votes from users 
-- LEFT JOIN votes 
-- ON (votes.voted_for=users.id)
-- WHERE (users.is_politician=true) AND (users.office_interested=2)
-- group by users.id;

-- END !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! END