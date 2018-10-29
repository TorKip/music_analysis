import sqlite3
from sqlite3 import Error


sqlite_create_spotify_song_table = """ CREATE TABLE IF NOT EXISTS songs (
        id integer PRIMARY KEY, 
        name text NOT NULL,
        etc text
    );"""


def create_connection(db_file):
    """ create database connection to SQlite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close
