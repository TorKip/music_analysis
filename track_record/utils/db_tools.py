import sqlite3
from sqlite3 import Error
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine

from contextlib import closing


SQLITE_CREATE_SPOTIFY_ARTISTS_TABLE = """ CREATE TABLE IF NOT EXISTS artists (
        id integer PRIMARY KEY,
        artist_name text NOT NULL,
        mbid text,
        spid text,
        misc text
    );"""

SQLITE_CREATE_SPOTIFY_ALBUMS_TABLE = """ CREATE TABLE IF NOT EXISTS albums (
        id integer PRIMARY KEY,
        album_name text NOT NULL,
        mbid text,
        spid text,
        artist_id integer,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    );"""

SQLITE_CREATE_SPOTIFY_TRACKS_TABLE = """ CREATE TABLE IF NOT EXISTS tracks (
        id integer PRIMARY KEY,
        track_name text NOT NULL,
        mbid text,
        spid text,
        album_id integer,
        FOREIGN KEY (album_id) REFERENCES albums (id)
    );"""

SQLITE_CREATE_SPOTIFY_LISTENS_TABLE = """ CREATE TABLE IF NOT EXISTS listens (
        id integer PRIMARY KEY,
        track_id integer,
        album_id integer,
        artist_id integer,
        end_time text,
        uts_end_time integer,
        FOREIGN KEY (track_id) REFERENCES tracks (id)
    );"""


def create_connection(db_file):
    """ create database connection to SQlite database """
    try:
        conn = sqlite3.connect(db_file)
        print("sqlite version: " + sqlite3.version)
        create_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        conn.close()
    except Error as e:
        print(e)


def get_connectable(db_filepath):
    """Returns sqlalchemy connectable(?), returning None if it fails."""
    try:
        eng = create_engine("sqlite:///{}".format(db_filepath))
        return eng
    except Error as error:
        print(error)
        return None


def create_table(cur, create_table_sql):
    """Creates a table given a db cursor and sql"""
    try:
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tables(conn):
    """Creates tables for artists, albums, tracks and listens"""
    cur = conn.cursor()
    create_table(cur, SQLITE_CREATE_SPOTIFY_ARTISTS_TABLE)
    create_table(cur, SQLITE_CREATE_SPOTIFY_ALBUMS_TABLE)
    create_table(cur, SQLITE_CREATE_SPOTIFY_TRACKS_TABLE)
    create_table(cur, SQLITE_CREATE_SPOTIFY_LISTENS_TABLE)


def execute_static_query(db_filepath, sql):
    """Executes a query without input data"""
    with closing(sqlite3.connect(db_filepath)) as conn:
        with conn:
            # with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
    return result


def execute_query(db_filepath, sql, args):
    """Executes a query on the given database
    TODO: implement checks and safeguards
    """
    with closing(sqlite3.connect(db_filepath)) as conn:
        with conn:
            # with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            cur.execute(sql, args)
            result = cur.fetchall()
    return result


def add_listen(cur, end_time, track_id, album_id, artist_id, uts_end_time=0):
    """Creates db entry for a listen"""
    sql = """ INSERT INTO listens(end_time, uts_end_time, track_id, album_id, artist_id)
            VALUES (?,?,?,?,?)"""
    listen = (end_time, uts_end_time, track_id, album_id, artist_id)
    cur.execute(sql, listen)
    return cur.lastrowid


def add_track(cur, track_name, mbid="", spid="", album_id=None):
    """Creates db entry for a track"""
    sql = """ INSERT INTO tracks(track_name, mbid, spid, album_id)
        VALUES(?,?,?,?) """
    track = (track_name, mbid, spid, album_id)
    cur.execute(sql, track)
    return cur.lastrowid


def add_album(cur, album_name, mbid="", spid="", artist_id=None):
    """Creates db entry for an album"""
    sql = """ INSERT INTO albums(album_name, mbid, spid, artist_id)
            VALUES (?,?,?,?) """
    album = (album_name, mbid, spid, artist_id)
    cur.execute(sql, album)
    return cur.lastrowid


def add_artist(cur, artist_name, mbid="", spid="", misc=""):
    """Creates db entry for an artist"""
    sql = """ INSERT INTO artists(artist_name, mbid, spid, misc)
        VALUES (?,?,?,?) """
    artist = (artist_name, mbid, spid, misc)
    cur.execute(sql, artist)
    return cur.lastrowid


def get_artists(cur, artist_id=None):
    """returns artist based on id, or all if none is given"""
    if not artist_id:
        sql = """ SELECT * from artists  ORDER BY artist_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from artists WHERE id=?"""
        cur.execute(sql, artist_id)
    return cur.fetchall()


def get_albums(cur, album_id=None):
    """returns album based on id, or all if none is given"""
    if not album_id:
        sql = """ SELECT * from albums ORDER BY album_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from albums WHERE id=?"""
        cur.execute(sql, album_id)
    return cur.fetchall()


def get_tracks(cur, track_id=None):
    """returns track based on id, or all if none is given"""
    if not track_id:
        sql = """ SELECT * FROM tracks ORDER BY track_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from tracks WHERE id=?"""
        cur.execute(sql, track_id)
    return cur.fetchall()


def get_listens(cur, id=None):
    """returns listen based on id, or all if none is given"""
    if not id:
        sql = """ SELECT * from listens ORDER BY end_time"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from listens where id=?"""
        cur.execute(sql, id)
    return cur.fetchall()


def get_all_data_ids(cur):
    """Returns all ids currently in the database"""
    artists_sql = """ SELECT id, artist_name FROM artists """
    albums_sql = """ SELECT id, album_name, artist_id FROM albums """
    tracks_sql = """ SELECT id, track_name, album_id FROM tracks """
    listens_sql = """ SELECT id, end_time, track_id FROM listens """

    cur.execute(artists_sql)
    artists = cur.fetchall()
    cur.execute(albums_sql)
    albums = cur.fetchall()
    cur.execute(tracks_sql)
    tracks = cur.fetchall()
    cur.execute(listens_sql)
    listens = cur.fetchall()

    artist_id_dict = {x[0]: x[1] for x in artists}
    artist_key_dict = {x[1]: x[0] for x in artists}

    album_id_dict = {}
    album_key_dict = {}
    track_id_dict = {}
    track_key_dict = {}
    listen_key_dict = {}

    for a in albums:
        album_id = a[0]
        album_name = a[1]
        artist_key = artist_id_dict[a[2]]
        album_key = artist_key + album_name
        album_id_dict[album_id] = album_key
        album_key_dict[album_key] = album_id

    for t in tracks:
        track_id = t[0]
        track_name = t[1]
        album_key = album_id_dict[t[2]]
        track_key = album_key + track_name
        track_id_dict[track_id] = track_key
        track_key_dict[track_key] = track_id

    for l in listens:
        listen_id = l[0]
        listen_date = l[1]
        track_key = track_id_dict[l[2]]
        listen_key = track_key + listen_date
        listen_key_dict[listen_key] = listen_id

    return artist_key_dict, album_key_dict, track_key_dict, listen_key_dict


def fill_tables(json_data, db_filename):
    """Fills db with data, checking if it already exists in db"""
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    tracks = {}
    albums = {}
    artists = {}
    listens = {}

    artists, albums, tracks, listens = get_all_data_ids(cur)

    for element in json_data:
        date = element["date"]
        uts_date = element["uts_date"]
        artist = element["artist"]
        album = element["album"]
        track = element["track"]

        artist_key = artist["name"]
        album_key = artist_key + album["name"]
        track_key = album_key + track["name"]
        listen_key = track_key + date

        if artist_key not in artists.keys():
            artist_id = add_artist(cur, artist["name"], artist["mbid"])
            artists[artist_key] = artist_id

            album_id = add_album(cur, album["name"], album["mbid"],
                                 artist_id=artist_id)
            albums[album_key] = album_id

            track_id = add_track(cur, track["name"], track["mbid"],
                                 album_id=album_id)
            tracks[track_key] = track_id

            listen_id = add_listen(cur, date, track_id, album_id,
                                   artist_id)
            listens[listen_key] = listen_id
        else:
            artist_id = artists[artist["name"]]

            if album_key not in albums.keys():
                album_id = add_album(cur, album["name"], album["mbid"],
                                     artist_id=artist_id)
                albums[album_key] = album_id

                track_id = add_track(cur, track["name"], track["mbid"],
                                     album_id=album_id)
                tracks[track_key] = track_id

                listen_id = add_listen(cur, date, track_id, album_id, 
                                       artist_id)

                listens[listen_key] = listen_id
            else:
                album_id = albums[album_key]

                if track_key not in tracks.keys():
                    track_id = add_track(cur, track["name"], track["mbid"],
                                         album_id=album_id)
                    tracks[track_key] = track_id

                    listen_id = add_listen(cur, date, track_id,
                                           album_id, artist_id)
                    listens[listen_key] = listen_id
                else:
                    track_id = tracks[track_key]

                    if listen_key not in listens.keys():
                        listen_id = add_listen(cur, date, track_id, 
                                               album_id, artist_id,
                                               uts_end_time=uts_date)
                        listens[listen_key] = listen_id
                    else:
                        listen_id = listens[listen_key]

    conn.commit()
    conn.close()
