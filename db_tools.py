import sqlite3
from sqlite3 import Error


sqlite_create_spotify_track_table = """ CREATE TABLE IF NOT EXISTS songs (
        id integer PRIMARY KEY, 
        spotifyId = text,
        spotifyURI = text,
        spotifyURL = text,
        trackName = text NOT NULL,
        # playDates = key to datelist....
        # artist key something
        # album  key somehting
        etc text
    );"""


def create_database(db_file="historyDB"):
    """ create database connection to SQlite database """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute(sqlite_create_spotify_track_table)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close

def add_track(db_file, track_dict):
    add_track_string = """ somthing or other around here """
    
    try:
        conn = sqlite3.connect(db_file)
        conn.execute(add_track_string)
    except Error as e:
        print(e)
    finally:
        conn.close()
