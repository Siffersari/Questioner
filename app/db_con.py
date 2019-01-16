import os
import psycopg2
from flask import current_app


def connect_to_database_url(url):
    """
    Takes in a database url and connect to it and returns
    an instance of the connection
    """

    conn = psycopg2.connect(url)

    return conn


def destroy_database():
    """ Drops all tables if exists """

    conn = connect_to_database_url(os.getenv('DATABASE_TESTING_URL'))

    curr = conn.cursor()

    curr.execute("DROP SCHEMA public CASCADE;")
    curr.execute("CREATE SCHEMA public;")
    curr.execute("GRANT USAGE ON SCHEMA public TO postgres;")

    conn.commit()


def create_table_users():
    """ 
    contains all the commands as a list
    """

    users = """ CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY NOT NULL,
    firstname VARCHAR (20) NOT NULL, lastname VARCHAR (20) NOT NULL, othername VARCHAR (20),
    email VARCHAR (30) NOT NULL, phone_number VARCHAR (20), username VARCHAR (20) NOT NULL,
    registered_on TIMESTAMP NOT NULL DEFAULT current_timestamp, password VARCHAR (256) NOT NULL,
    roles VARCHAR (20) DEFAULT false
    );"""

    meetups = """ CREATE TABLE IF NOT EXISTS meetups (meetup_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL, topic VARCHAR (150) NOT NULL,happening_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
    location VARCHAR (100) NOT NULL,created_on TIMESTAMP NOT NULL DEFAULT current_timestamp
    ); """

    questions = """ CREATE TABLE IF NOT EXISTS questions (question_id serial PRIMARY KEY NOT NULL,
    meetup_id INTEGER NOT NULL, user_id INTEGER NOT NULL, title VARCHAR (150) NOT NULL,
    body VARCHAR (1000) NOT NULL, votes INTEGER DEFAULT 0,
    created_on TIMESTAMP NOT NULL DEFAULT current_timestamp
    ); """

    rsvps = """ CREATE TABLE IF NOT EXISTS rsvps (rsvp_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL, meetup_id INTEGER NOT NULL, response VARCHAR (20),
    responded_on TIMESTAMP NOT NULL DEFAULT current_timestamp
    ); """

    comments = """ CREATE TABLE IF NOT EXISTS comments (comment_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL, question_id INTEGER NOT NULL, comments VARCHAR (1000), 
    commented_on TIMESTAMP NOT NULL DEFAULT current_timestamp
    ); """

    tags = """ CREATE TABLE IF NOT EXISTS tags (tags_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL, meetup_id INTEGER NOT NULL, tags VARCHAR [200]
    ); """

    images = """ CREATE TABLE IF NOT EXISTS images (image_id serial PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL, meetup_id INTEGER NOT NULL, images VARCHAR[]
    ); """

    blacklist = """ CREATE TABLE IF NOT EXISTS blacklisted (tokens VARCHAR (256) NOT NULL); """

    return [users, meetups, questions, rsvps, comments, tags, images, blacklist]


def create_tables():
    """ 
    Takes an argument with two possible values 'main' or 'testing'
    & initializes the app's main database if 'main' or testing database if 
    'testing' is passed"""

    db_url = current_app.config['DATABASE_URL']

    conn = connect_to_database_url(db_url)

    curr = conn.cursor()

    data = create_table_users()

    for i in data:
        curr.execute(i)
        conn.commit()

    return conn


def init_test_db():
    """ 
    Sets up database for testing 
    """
    destroy_database()

    conn = connect_to_database_url(os.getenv("DATABASE_TESTING_URL"))

    curr = conn.cursor()

    data = create_table_users()

    for i in data:
        curr.execute(i)
        conn.commit()

    return conn
