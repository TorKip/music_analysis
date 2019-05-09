"""Module for handling tests on the database
"""
from os import remove
import sqlite3
from track_record.preprocess.preprocess import fill_database
from track_record.utils.db_tools import create_connection, get_listens,\
    get_tracks, get_albums, get_artists

# sqlite3

TEST_DATA = "track_record/tests/test_data.json"
DB_FILENAME = "test_database.db"


def create_test_database():
    """Creates a temporary database for testing"""
    print("Creating test database")
    create_connection(DB_FILENAME)


def delete_test_database():
    """Deletes test database"""
    print("Deleting test_database...")
    remove(DB_FILENAME)
    print("test_database deleted.")


def test_database_fill():
    """Fills database with testing data"""
    fill_database(TEST_DATA, DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    # ar, al, tr, li = get_all_data_ids(cur)
    listens = get_listens(cur)
    tracks = get_tracks(cur)
    albums = get_albums(cur)
    artists = get_artists(cur)
    conn.close()

    print("listens:\n{}\n".format(listens))
    print("tracks: \n{}\n".format(tracks))
    print("albums:\n{}\n".format(albums))
    print("artists:\n{}\n".format(artists))
