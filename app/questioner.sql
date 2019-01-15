CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    firstname VARCHAR (20) NOT NULL,
    lastname VARCHAR (20) NOT NULL,
    othername VARCHAR (20),
    email VARCHAR (30) NOT NULL,
    phone_number VARCHAR (20),
    username VARCHAR (20) NOT NULL,
    registered_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
    password VARCHAR (256) NOT NULL,
    is_admin BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS meetups (
    meetup_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    topic VARCHAR (150) NOT NULL,
    happening_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
    location VARCHAR (100) NOT NULL,
    images VARCHAR[],
    tags VARCHAR [200],
    created_on TIMESTAMP NOT NULL DEFAULT current_timestamp

);

CREATE TABLE IF NOT EXISTS questions (
    question_id serial PRIMARY KEY NOT NULL,
    meetup_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title VARCHAR (150) NOT NULL,
    body VARCHAR (1000) NOT NULL,
    votes INTEGER DEFAULT 0,
    comments VARCHAR (1000),
    created_on TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS rsvps (
    rsvp_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    meetup_id INTEGER NOT NULL,
    response VARCHAR (20)  
);
