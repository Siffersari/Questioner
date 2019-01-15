import os
import psycopg2
from flask import current_app


def connect_to_database_url(url):
    """ 
    Takes in a database url and uses psycopg2
    to create a connection
    """

    conn = psycopg2.connect(url)

    return conn


def destroy_database():
    """ 
    Destroys all the tables in the testing
    database if any exists
    """

    conn = connect_to_database_url(os.getenv('DATABASE_TESTING_URL'))

    curr = conn.cursor()

    curr.execute("DROP SCHEMA public CASCADE;")
    curr.execute("CREATE SCHEMA public;")
    curr.execute("GRANT USAGE ON SCHEMA public TO leewel;")

    conn.commit()


def create_tables(db_type="main"):
    """ Accepts two possible values
    main or testing & initializes the main database
    or testing database respectively """

    db_url = current_app.config['DATABASE_URL']

    if db_type == "testing":
        destroy_database()
        db_url = os.getenv('DATABASE_TESTING_URL')

    conn = connect_to_database_url(db_url)

    curr = conn.cursor()

    pass
