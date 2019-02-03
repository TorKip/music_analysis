import sqlite3
from sqlite3 import Error


sqlite_create_spotify_artists_table = """ CREATE TABLE IF NOT EXISTS artists (
        id integer PRIMARY KEY,
        artist_name text NOT NULL,
        mbid text,
        spid text,
        misc text
    );"""

sqlite_create_spotify_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
        id integer PRIMARY KEY,
        album_name text NOT NULL,
        mbid text,
        spid text,
        artist_id integer,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    );"""

sqlite_create_spotify_tracks_table = """ CREATE TABLE IF NOT EXISTS tracks (
        id integer PRIMARY KEY, 
        track_name text NOT NULL,
        mbid text,
        spid text,
        album_id integer,
        FOREIGN KEY (album_id) REFERENCES albums (id),
    );"""

sqlite_create_spotify_listens_table = """ CREATE TABLE IF NOT EXISTS listens (
        id integer PRIMARY KEY,
        track_id integer,
        end_time text,
        FOREIGN KEY (track_id) REFERENCES tracks (id)
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
    create_table(conn, sqlite_create_spotify_tracks_table)
    create_table(conn, sqlite_create_spotify_listens_table)

def add_listen(conn, end_time, track_id):
    sql = """ INSERT INTO listens(end_time, track_id) VALUES (?,?)"""
    listen = (end_time, track_id)
    cur = conn.cursor()
    cur.execute(sql, listen)
    return cur.lastrowid

def add_track(conn, track_name, mbid="", spid="", end_time="", artist_id=None, album_id=None):
    sql = """ INSERT INTO tracks(track_name, mbid, spid, end_time, artist_id, album_id) VALUES(?,?,?,?,?,?) """
    track = (track_name, mbid, spid, end_time, artist_id, album_id)
    cur = conn.cursor()
    cur.execute(sql, track)
    return cur.lastrowid

def add_album(conn, album_name, mbid="", spid="", artist_id=None):
    sql = """ INSERT INTO albums(album_name, mbid, spid, artist_id) VALUES (?,?,?,?) """
    album = (album_name, mbid, spid, artist_id)
    cur = conn.cursor()
    cur.execute(sql, album)
    return cur.lastrowid
    
def add_artist(conn, artist_name, mbid="", spid="", misc=""):
    sql = """ INSERT INTO albums(artist_name, mbid, spid, misc) VALUES (?,?,?,?) """
    artist = (artist_name, mbid, spid, misc)
    cur = conn.cursor()
    cur.execute(sql, artist)
    return cur.lastrowid
