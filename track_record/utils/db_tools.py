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
        FOREIGN KEY (album_id) REFERENCES albums (id)
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
        print("sqlite version: "+ sqlite3.version)
        create_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        conn.close()
    except Error as e:
        print(e)
    

def create_table(cur, create_table_sql):
    try:
        cur.execute(create_table_sql)
    except Error as e:
        print(e)

def create_tables(conn):
    cur = conn.cursor()
    create_table(cur, sqlite_create_spotify_artists_table)
    create_table(cur, sqlite_create_spotify_albums_table)
    create_table(cur, sqlite_create_spotify_tracks_table)
    create_table(cur, sqlite_create_spotify_listens_table)

def add_listen(cur, end_time, track_id):
    sql = """ INSERT INTO listens(end_time, track_id) VALUES (?,?)"""
    listen = (end_time, track_id)
    cur.execute(sql, listen)
    return cur.lastrowid

def add_track(cur, track_name, mbid="", spid="", album_id=None):
    sql = """ INSERT INTO tracks(track_name, mbid, spid, album_id) VALUES(?,?,?,?) """
    track = (track_name, mbid, spid, album_id)
    cur.execute(sql, track)
    return cur.lastrowid

def add_album(cur, album_name, mbid="", spid="", artist_id=None):
    sql = """ INSERT INTO albums(album_name, mbid, spid, artist_id) VALUES (?,?,?,?) """
    album = (album_name, mbid, spid, artist_id)
    cur.execute(sql, album)
    return cur.lastrowid
    
def add_artist(cur, artist_name, mbid="", spid="", misc=""):
    sql = """ INSERT INTO artists(artist_name, mbid, spid, misc) VALUES (?,?,?,?) """
    artist = (artist_name, mbid, spid, misc)
    cur.execute(sql, artist)
    return cur.lastrowid


def get_artists(cur, artist_id=None):
    if not artist_id:
        sql = """ SELECT * from artists  ORDER BY artist_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from artists WHERE id=? ORDER BY artist_name"""
        cur.execute(sql, artist_id)
    return cur.fetchall()

def get_albums(cur, album_id=None):
    if not album_id:
        sql = """ SELECT * from albums ORDER BY album_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from albums WHERE id=? ORDER BY album_name"""
        cur.execute(sql, album_id)
    return cur.fetchall()

def get_tracks(cur, track_id=None):
    if not track_id:
        sql = """ SELECT * FROM tracks ORDER BY track_name"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from tracks WHERE id=? ORDER BY track_name"""
        cur.execute(sql, track_id)
    return cur.fetchall()

def get_listens(cur, id=None):
    
    if not id:
        sql = """ SELECT * from listens ORDER BY end_time"""
        cur.execute(sql)
    else:
        sql = """ SELECT * from listens where id=? ORDER BY end_time"""
        cur.execute(sql, id)
    return cur.fetchall()

def get_all_data_ids(cur):

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

    artist_id_dict = {x[0]:x[1] for x in artists}
    artist_key_dict = {x[1]:x[0] for x in artists}

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
        track_key =  album_key + track_name
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
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    tracks = {}
    albums = {}
    artists = {}
    listens = {}

    artists, albums, tracks, listens = get_all_data_ids(cur)

    for element in json_data:
        date = element["date"]
        artist = element["artist"]
        album = element["album"]
        track = element["track"]
        
        artist_key = artist["name"]
        album_key = artist_key + album["name"]
        track_key = album_key + track["name"]
        listen_key = track_key + date

        if not artist_key in artists.keys():
            artist_id = add_artist(cur, artist["name"], artist["mbid"])
            artists[artist_key] = artist_id

            album_id = add_album(cur, album["name"], album["mbid"], artist_id=artist_id)
            albums[album_key] = album_id

            track_id = add_track(cur, track["name"], track["mbid"], album_id=album_id )
            tracks[track_key] = track_id 

            listen_id = add_listen(cur, date, track_id)
            listens[listen_key] = listen_id
        else:
            artist_id = artists[artist["name"]]

            if not album_key in albums.keys():
                album_id = add_album(cur, album["name"], album["mbid"], artist_id=artist_id)
                albums[album_key] = album_id

                track_id = add_track(cur, track["name"], track["mbid"], album_id=album_id )
                tracks[track_key] = track_id

                listen_id = add_listen(cur, date, track_id)
                listens[listen_key] = listen_id
            else:
                album_id = albums[album_key]

                if not track_key in tracks.keys():
                    track_id = add_track(cur, track["name"], track["mbid"], album_id=album_id )
                    tracks[track_key] = track_id   

                    listen_id = add_listen(cur, date, track_id)
                    listens[listen_key] = listen_id
                else:
                    track_id = tracks[track_key]

                    if not listen_key in listens.keys():
                        listen_id = add_listen(cur, date, track_id)
                        listens[listen_key] = listen_id
                    else:
                        listen_id = listens[listen_key]
    
    conn.commit()
    conn.close()
