import sqlite3
from sqlite3 import Error

'''
id primary key
str name - not null
str mbid
str etc
'''
'''
id primary key
str song name - not null
str mbid
date/int timeplayed
fkey artist
str etc
'''

sqlite_create_spotify_artists_table = """ CREATE TABLE IF NOT EXISTS artists (
        id integer PRIMARY KEY,
        name text NOT NULL,
        mbid text,
        spid text,
        misc text
    );"""

sqlite_create_spotify_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
        id integer PRIMARY KEY,
        name text NOT NULL,
        mbid text,
        spid text,
        artist_id integer,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
);"""

sqlite_create_spotify_songs_table = """ CREATE TABLE IF NOT EXISTS songs (
        id integer PRIMARY KEY, 
        name text NOT NULL,
        mbid text,
        spid text,
        end_time text,
        artist_id integer,
        album_id integer,
        FOREIGN KEY (artist_id) REFERENCES artists (id),
        FOREIGN KEY (album_id) PREFERENCES artists (id)
    );"""




def create_connection(db_file):
    """ create database connection to SQlite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        create_tables(conn)
    except Error as e:
        print(e)
    finally:
        conn.close

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_tables(conn):
    create_table(conn, sqlite_create_spotify_artists_table)
    create_table(conn, sqlite_create_spotify_albums_table)
    create_table(conn, sqlite_create_spotify_songs_table)

def add_song(conn, name, mbid="", spid="", end_time="", artist_id=None, album_id=None):
    sql = """ INSERT INTO songs(name, mbid, spid, end_time, artist_id, album_id) VALUES(?,?,?,?,?,?) """
    song = (name, mbid, spid, end_time, artist_id, album_id)
    cur = conn.cursor()
    cur.execute(sql, song)
    return cur.lastrowid

def add_album(conn, name, mbid="", spid="", artist_id=None):
    sql = """ INSERT INTO albums(name, mbid, spid, artist_id) VALUES (?,?,?,?) """
    album = (name, mbid, spid, artist_id)
    cur = conn.cursor()
    cur.execute(sql, album)
    return cur.lastrowid
    
def add_artist(conn, name, mbid="", spid="", misc=""):
    sql = """ INSERT INTO albums(name, mbid, spid, misc) VALUES (?,?,?,?) """
    artist = (name, mbid, spid, misc)
    cur = conn.cursor()
    cur.execute(sql, artist)
    return cur.lastrowid
