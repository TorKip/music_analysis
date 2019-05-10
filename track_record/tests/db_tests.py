"""Module for handling tests on the database
"""
from os import remove
import sqlite3 as sql3
import sqlalchemy as sqlal
import unittest
from json import loads
# from track_record.preprocess.preprocess import fill_database
# from track_record.utils.db_tools import create_connection, get_listens,\
import track_record.utils.db_tools as dbt
    # get_tracks, get_albums, get_artists

# sqlite3

# TEST_DATA = "track_record/tests/test_data.json"
# DB_FILENAME = "test_database.db"


# def create_test_database():
#     """Creates a temporary database for testing"""
#     print("Creating test database")
#     create_connection(DB_FILENAME)


# def delete_test_database():
#     """Deletes test database"""
#     print("Deleting test_database...")
#     remove(DB_FILENAME)
#     print("test_database deleted.")


# def test_database_fill():
#     """Fills database with testing data"""
#     fill_database(TEST_DATA, DB_FILENAME)
#     conn = sqlite3.connect(DB_FILENAME)
#     cur = conn.cursor()
#     # ar, al, tr, li = get_all_data_ids(cur)
#     listens = get_listens(cur)
#     tracks = get_tracks(cur)
#     albums = get_albums(cur)
#     artists = get_artists(cur)
#     conn.close()

#     print("listens:\n{}\n".format(listens))
#     print("tracks: \n{}\n".format(tracks))
#     print("albums:\n{}\n".format(albums))
#     print("artists:\n{}\n".format(artists))

def db_tool_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader.loadTestsFromTestCase(
        unittest.defaultTestLoader, TestDatabaseConnections))
    suite.addTest(unittest.TestLoader.loadTestsFromTestCase(
        unittest.defaultTestLoader, TestDatabaseInput))
    return suite


class TestDatabaseConnections(unittest.TestCase):
    database_name = "test_database.db"
    # sqlalchemy_db_filepath = "sqlite:///test_database.db"

    def test_database_creation(self):
        self.assertIsNone(dbt.create_connection(self.database_name))
        # self.assertFalse(True)

    def test_get_connectable(self):
        self.assertIsNotNone(dbt.get_connectable(self.database_name))

    @classmethod
    def tearDownClass(cls):
        remove(cls.database_name)
        return super().tearDownClass()


class TestDatabaseInput(unittest.TestCase):
    database_name = "test_database.db"
    @classmethod
    def setUpClass(cls):
        try:
            # make sure the database is empty
            remove(cls.database_name)
        except FileNotFoundError:
            pass
        cls.db_connection = sql3.connect(cls.database_name)
        cls.db_cursor = cls.db_connection.cursor()
        dbt.create_tables(cls.db_connection)
        # with open("track_record/tests/test_data.json", 'r',
        #     encoding='utf-8') as test_json:
        #     cls.json_data = load(test_json)
        cls.json_data = loads(TEST_JSON_DATA)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.db_connection.close()
        remove(cls.database_name)
        return super().tearDownClass()

    def run(self, result):
        return super().run(result)

    def test_0_add_artist(self):
        self.assertEqual(dbt.add_artist(self.db_cursor,
            "artist_1_name", mbid="0", spid="0",
            misc="misc info about artist"), 1)
    
    def test_1_add_album(self):
        self.assertEqual(dbt.add_album(self.db_cursor,
            "album_1_name", 1, mbid="0", spid="0"), 1)

    def test_2_add_track(self):
        self.assertEqual(dbt.add_track(self.db_cursor,
            "track_1_name", 1, mbid="0", spid="0"), 1)

    def test_3_add_listen(self):
        self.assertEqual(dbt.add_listen(self.db_cursor,
            "2017-12-28 19:48", 1, 1, 1, "1514488440"), 1)

    # Fix this test or fix the method
    def test_4_fill_tables(self):
        self.assertIsNone(dbt.fill_tables(self.json_data,
            cursor=self.db_cursor))

    # def test_something(self):
    #     self.assertFalse(True)


class TestDatabaseReading(unittest.TestCase):
    pass


TEST_JSON_DATA = """
[
    {
        "date": "2017-12-30 14:13",
        "uts_date": "1514643180",
        "artist": {
            "name": "Moddi",
            "mbid": "8afb628a-ab5f-405a-8759-fc03e462fe40"
        },
        "track": {
            "name": "Nordnorsk Julesalme",
            "mbid": "",
            "end_time": "2017-12-30 14:13",
            "artist_id": "8afb628a-ab5f-405a-8759-fc03e462fe40",
            "album_id": ""
        },
        "album": {
            "name": "Vi tenner våre lykter (Streaming)",
            "mbid": "",
            "artist_id": "8afb628a-ab5f-405a-8759-fc03e462fe40"
        }
    },
    {
        "date": "2017-12-28 19:24",
        "uts_date": "1514489040",
        "artist": {
            "name": "Hans Zimmer",
            "mbid": "e6de1f3b-6484-491c-88dd-6d619f142abc"
        },
        "track": {
            "name": "This Land",
            "mbid": "487051ab-49f9-4e2f-97ba-66203e9b2633",
            "end_time": "2017-12-28 19:24",
            "artist_id": "e6de1f3b-6484-491c-88dd-6d619f142abc",
            "album_id": ""
        },
        "album": {
            "name": "The Lion King: Special Edition Original Soundtrack (English Version)",
            "mbid": "",
            "artist_id": "e6de1f3b-6484-491c-88dd-6d619f142abc"
        }
    },
    {
        "date": "2017-12-28 19:21",
        "uts_date": "1514488860",
        "artist": {
            "name": "Howard Shore",
            "mbid": "9b58672a-e68e-4972-956e-a8985a165a1f"
        },
        "track": {
            "name": "Forth Eorlingas",
            "mbid": "25b03833-74cc-4612-84d1-085f096cd2fe",
            "end_time": "2017-12-28 19:21",
            "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f",
            "album_id": ""
        },
        "album": {
            "name": "The Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)",
            "mbid": "",
            "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f"
        }
    },
    {
        "date": "2017-12-28 19:14",
        "uts_date": "1514488440",
        "artist": {
            "name": "Howard Shore",
            "mbid": "9b58672a-e68e-4972-956e-a8985a165a1f"
        },
        "track": {
            "name": "The Breaking of the Fellowship",
            "mbid": "",
            "end_time": "2017-12-28 19:14",
            "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f",
            "album_id": ""
        },
        "album": {
            "name": "The Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)",
            "mbid": "",
            "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f"
        }
    },
    {
        "date": "2017-12-28 19:12",
        "uts_date": "1514488320",
        "artist": {
            "name": "Ramin Djawadi",
            "mbid": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
        },
        "track": {
            "name": "Main Title",
            "mbid": "03a20b59-72ea-4806-9518-a481a54ad144",
            "end_time": "2017-12-28 19:12",
            "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1",
            "album_id": ""
        },
        "album": {
            "name": "Game Of Thrones",
            "mbid": "",
            "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
        }
    },
    {
        "date": "2017-12-28 19:10",
        "uts_date": "1514488200",
        "artist": {
            "name": "Ramin Djawadi",
            "mbid": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
        },
        "track": {
            "name": "Main Title",
            "mbid": "03a20b59-72ea-4806-9518-a481a54ad144",
            "end_time": "2017-12-28 19:12",
            "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1",
            "album_id": ""
        },
        "album": {
            "name": "Game Of Thrones",
            "mbid": "",
            "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
        }
    },
    {
        "date": "2017-12-28 19:00",
        "uts_date": "1514487600",
        "artist": {
            "name": "Ramin Djawadi",
            "mbid": ""
        },
        "track": {
            "name": "Main Title",
            "mbid": "",
            "end_time": "2017-12-28 19:00",
            "artist_id": "",
            "album_id": ""
        },
        "album": {
            "name": "West world",
            "mbid": "",
            "artist_id": ""
        }
    },
    {
        "date": "2017-12-28 18:50",
        "uts_date": "1514487000",
        "artist": {
            "name": "Floppotron covers",
            "mbid": ""
        },
        "track": {
            "name": "Main Title",
            "mbid": "",
            "end_time": "2017-12-28 18:50",
            "artist_id": "",
            "album_id": ""
        },
        "album": {
            "name": "West world",
            "mbid": "",
            "artist_id": ""
        }
    }
]
"""
