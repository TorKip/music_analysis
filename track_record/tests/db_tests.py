"""Module for handling tests on the database
"""
from os import remove
import sqlite3 as sql3
# import sqlalchemy as sqlal
import unittest
from json import load
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
    load_testCase = unittest.TestLoader.loadTestsFromTestCase
    test_loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(load_testCase(
        test_loader, TestDatabaseConnections))
    suite.addTest(load_testCase(
        test_loader, TestDatabaseInput))
    suite.addTest(load_testCase(
        test_loader, TestDatabaseReading))
    return suite


class TestDatabaseConnections(unittest.TestCase):
    database_name = "track_record/tests/temp_test_database.db"
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
    database_name = "track_record/tests/temp_test_database.db"
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
        with open("track_record/tests/static_test_data.json", 'r',
            encoding='utf-8') as test_json:
            cls.json_data = load(test_json)
        # cls.json_data = loads(TEST_JSON_DATA)
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

    def test_4_fill_tables(self):
        self.assertIsNone(dbt.fill_tables(self.json_data,
            cursor=self.db_cursor))

    # def test_something(self):
    #     self.assertFalse(True)


class TestDatabaseReading(unittest.TestCase):
    database_name = "track_record/tests/static_test_database.db"
    @classmethod
    def setUpClass(cls):
        try:
            cls.db_connection = sql3.connect(cls.database_name)
            cls.db_cursor = cls.db_connection.cursor()
        except Exception as e:
            print(e)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.db_connection.close()
        return super().tearDownClass()

    def test_get_artists(self):
        expected_artists = [
            (8, 'Brian Tyler', '30480808-4c03-432c-9e94-dd3b12d4e127', '', ''),
            (2, 'Hans Zimmer', 'e6de1f3b-6484-491c-88dd-6d619f142abc', '', ''),
            (3, 'Howard Shore', '9b58672a-e68e-4972-956e-a8985a165a1f', '', ''),
            (5, 'John Powell', '52bb713d-b0c9-4bf6-9f58-392388d5cc11', '', ''),
            (7, 'Kamelot', '46f4cd77-8870-4ad8-a205-1bee18901d0f', '', ''),
            (1, 'Moddi', '8afb628a-ab5f-405a-8759-fc03e462fe40', '', ''),
            (6, 'Pyotr Ilyich Tchaikovsky', '9ddd7abc-9e1b-471d-8031-583bc6bc8be9', '', ''),
            (4, 'Ramin Djawadi', 'f089f636-6b85-4e0e-a192-0d30ed2b44d1', '', '')
            ]
        artist_2 = (2, 'Hans Zimmer', 'e6de1f3b-6484-491c-88dd-6d619f142abc', '', '')
        self.assertEqual(dbt.get_artists(self.db_cursor), expected_artists)
        self.assertEqual(dbt.get_artists(self.db_cursor, artist_id=2), [artist_2])

    def test_get_albums(self):
        expected_albums = [
            (5, 'Game Of Thrones (Music From The HBO Series)', '', '', 4),
            (9, 'Hans Zimmer - The Classics', '', '', 2),
            (6, 'How To Train Your Dragon (Music From The Motion Picture)', '', '', 5),
            (10, 'Karma', 'dcaa1f02-3bad-4337-be7e-c769fd9df9e7', '', 7),
            (8, 'Tchaikovsky: Ballet Suites (Swan Lake; The Sleeping Beauty; The Nutcraker)', '', '', 6),
            (2, 'The Lion King: Special Edition Original Soundtrack (English Version)', '', '', 2),
            (3, 'The Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)', '', '', 3),
            (4, 'The Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)', '', '', 3),
            (11, 'Thor: The Dark World (Original Motion Picture Soundtrack)', '', '', 8),
            (1, 'Vi tenner våre lykter (Streaming)', '', '', 1),
            (7, 'Westworld: Season 1 (Music from the HBO® Series)', '', '', 4)
            ]
        album_2 = (2, 'The Lion King: Special Edition Original Soundtrack (English Version)', '', '', 2)
        self.assertEqual(dbt.get_albums(self.db_cursor), expected_albums)
        self.assertEqual(dbt.get_albums(self.db_cursor, album_id=2), [album_2])

    def test_get_tracks(self):
        expected_tracks = [
            (9, 'Concerning Hobbits', 'c5475b37-51fc-45b4-af9d-4f4b867510b3', '', 4),
            (3, 'Forth Eorlingas', '25b03833-74cc-4612-84d1-085f096cd2fe', '', 3),
            (12, 'Karma', '7285a347-8b17-4059-a4a3-18911bdc3263', '', 10),
            (5, 'Main Title', '03a20b59-72ea-4806-9518-a481a54ad144', '', 5),
            (8, 'Main Title Theme - Westworld', '', '', 7),
            (1, 'Nordnorsk Julesalme', '', '', 1),
            (7, 'Paint It Black', '', '', 7),
            (10, 'Swan Lake (Suite), Op.20a, TH 219: 1. Scene - Swan Theme', '', '', 8),
            (6, 'Test Drive', '704c91a8-bfa8-4a02-bc21-f68984ea73c8', '', 6),
            (4, 'The Breaking of the Fellowship - Feat. "In Dreams"', '', '', 4),
            (2, 'This Land', '487051ab-49f9-4e2f-97ba-66203e9b2633', '', 2),
            (11, 'This Land (from "The Lion King")', '', '', 9),
            (13, 'Thor: The Dark World', '3889cfc0-8c59-4abd-8bc5-6ddd6c6512e0', '', 11)
            ]
        track_2 = (2, 'This Land', '487051ab-49f9-4e2f-97ba-66203e9b2633', '', 2)
        self.assertEqual(dbt.get_tracks(self.db_cursor), expected_tracks)
        self.assertEqual(dbt.get_tracks(self.db_cursor, track_id=2), [track_2])

    def test_get_listens(self):
        expected_listens = [
            (15, 13, 11, 8, '2017-09-20 14:42', 1505918555),
            (14, 7, 7, 4, '2017-09-27 16:44', 1506530695),
            (13, 12, 10, 7, '2017-10-02 20:55', 1506977709),
            (12, 6, 6, 5, '2017-11-12 10:45', 1510483501),
            (11, 11, 9, 2, '2017-11-30 07:56', 1512028579),
            (10, 10, 8, 6, '2017-12-12 09:54', 1513072450),
            (9, 9, 4, 3, '2017-12-12 10:11', 1513073517),
            (8, 8, 7, 4, '2017-12-12 10:17', 1513073849),
            (7, 7, 7, 4, '2017-12-12 10:26', 1513074368),
            (6, 6, 6, 5, '2017-12-28 19:08', 1514488139),
            (5, 5, 5, 4, '2017-12-28 19:12', 1514488350),
            (4, 4, 4, 3, '2017-12-28 19:14', 1514488456),
            (3, 3, 3, 3, '2017-12-28 19:21', 1514488898),
            (2, 2, 2, 2, '2017-12-28 19:24', 1514489094),
            (1, 1, 1, 1, '2017-12-30 14:13', 1514643212)
            ]
        listen_2 = (2, 2, 2, 2, '2017-12-28 19:24', 1514489094)
        self.assertEqual(dbt.get_listens(self.db_cursor), expected_listens)
        self.assertEqual(dbt.get_listens(self.db_cursor, id=2), [listen_2])

    def test_get_all_ids(self):
        artist_dict = {
            'Moddi': 1,
            'Hans Zimmer': 2,
            'Howard Shore': 3,
            'Ramin Djawadi': 4,
            'John Powell': 5,
            'Pyotr Ilyich Tchaikovsky': 6,
            'Kamelot': 7,
            'Brian Tyler': 8
            }
        album_dict = {
            'ModdiVi tenner våre lykter (Streaming)': 1,
            'Hans ZimmerThe Lion King: Special Edition Original Soundtrack (English Version)': 2,
            'Howard ShoreThe Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)': 3,
            'Howard ShoreThe Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)': 4,
            'Ramin DjawadiGame Of Thrones (Music From The HBO Series)': 5,
            'John PowellHow To Train Your Dragon (Music From The Motion Picture)': 6,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)': 7,
            'Pyotr Ilyich TchaikovskyTchaikovsky: Ballet Suites (Swan Lake; The Sleeping Beauty; The Nutcraker)': 8,
            'Hans ZimmerHans Zimmer - The Classics': 9,
            'KamelotKarma': 10,
            'Brian TylerThor: The Dark World (Original Motion Picture Soundtrack)': 11
            }
        tracks_dict = {
            'ModdiVi tenner våre lykter (Streaming)Nordnorsk Julesalme': 1,
            'Hans ZimmerThe Lion King: Special Edition Original Soundtrack (English Version)This Land': 2,
            'Howard ShoreThe Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)Forth Eorlingas': 3,
            'Howard ShoreThe Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)The Breaking of the Fellowship - Feat. "In Dreams"': 4,
            'Ramin DjawadiGame Of Thrones (Music From The HBO Series)Main Title': 5,
            'John PowellHow To Train Your Dragon (Music From The Motion Picture)Test Drive': 6,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)Paint It Black': 7,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)Main Title Theme - Westworld': 8,
            'Howard ShoreThe Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)Concerning Hobbits': 9,
            'Pyotr Ilyich TchaikovskyTchaikovsky: Ballet Suites (Swan Lake; The Sleeping Beauty; The Nutcraker)Swan Lake (Suite), Op.20a, TH 219: 1. Scene - Swan Theme': 10,
            'Hans ZimmerHans Zimmer - The ClassicsThis Land (from "The Lion King")': 11,
            'KamelotKarmaKarma': 12,
            'Brian TylerThor: The Dark World (Original Motion Picture Soundtrack)Thor: The Dark World': 13
            }
        listens_dict = {
            'ModdiVi tenner våre lykter (Streaming)Nordnorsk Julesalme2017-12-30 14:13': 1,
            'Hans ZimmerThe Lion King: Special Edition Original Soundtrack (English Version)This Land2017-12-28 19:24': 2,
            'Howard ShoreThe Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)Forth Eorlingas2017-12-28 19:21': 3,
            'Howard ShoreThe Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)The Breaking of the Fellowship - Feat. "In Dreams"2017-12-28 19:14': 4,
            'Ramin DjawadiGame Of Thrones (Music From The HBO Series)Main Title2017-12-28 19:12': 5,
            'John PowellHow To Train Your Dragon (Music From The Motion Picture)Test Drive2017-12-28 19:08': 6,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)Paint It Black2017-12-12 10:26': 7,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)Main Title Theme - Westworld2017-12-12 10:17': 8,
            'Howard ShoreThe Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)Concerning Hobbits2017-12-12 10:11': 9,
            'Pyotr Ilyich TchaikovskyTchaikovsky: Ballet Suites (Swan Lake; The Sleeping Beauty; The Nutcraker)Swan Lake (Suite), Op.20a, TH 219: 1. Scene - Swan Theme2017-12-12 09:54': 10,
            'Hans ZimmerHans Zimmer - The ClassicsThis Land (from "The Lion King")2017-11-30 07:56': 11,
            'John PowellHow To Train Your Dragon (Music From The Motion Picture)Test Drive2017-11-12 10:45': 12,
            'KamelotKarmaKarma2017-10-02 20:55': 13,
            'Ramin DjawadiWestworld: Season 1 (Music from the HBO® Series)Paint It Black2017-09-27 16:44': 14,
            'Brian TylerThor: The Dark World (Original Motion Picture Soundtrack)Thor: The Dark World2017-09-20 14:42': 15
            }
        self.assertEqual(
            dbt.get_all_data_ids(self.db_cursor),
            (artist_dict, album_dict, tracks_dict, listens_dict))


# TEST_JSON_DATA = """
# [
#     {
#         "date": "2017-12-30 14:13",
#         "uts_date": "1514643180",
#         "artist": {
#             "name": "Moddi",
#             "mbid": "8afb628a-ab5f-405a-8759-fc03e462fe40"
#         },
#         "track": {
#             "name": "Nordnorsk Julesalme",
#             "mbid": "",
#             "end_time": "2017-12-30 14:13",
#             "artist_id": "8afb628a-ab5f-405a-8759-fc03e462fe40",
#             "album_id": ""
#         },
#         "album": {
#             "name": "Vi tenner våre lykter (Streaming)",
#             "mbid": "",
#             "artist_id": "8afb628a-ab5f-405a-8759-fc03e462fe40"
#         }
#     },
#     {
#         "date": "2017-12-28 19:24",
#         "uts_date": "1514489040",
#         "artist": {
#             "name": "Hans Zimmer",
#             "mbid": "e6de1f3b-6484-491c-88dd-6d619f142abc"
#         },
#         "track": {
#             "name": "This Land",
#             "mbid": "487051ab-49f9-4e2f-97ba-66203e9b2633",
#             "end_time": "2017-12-28 19:24",
#             "artist_id": "e6de1f3b-6484-491c-88dd-6d619f142abc",
#             "album_id": ""
#         },
#         "album": {
#             "name": "The Lion King: Special Edition Original Soundtrack (English Version)",
#             "mbid": "",
#             "artist_id": "e6de1f3b-6484-491c-88dd-6d619f142abc"
#         }
#     },
#     {
#         "date": "2017-12-28 19:21",
#         "uts_date": "1514488860",
#         "artist": {
#             "name": "Howard Shore",
#             "mbid": "9b58672a-e68e-4972-956e-a8985a165a1f"
#         },
#         "track": {
#             "name": "Forth Eorlingas",
#             "mbid": "25b03833-74cc-4612-84d1-085f096cd2fe",
#             "end_time": "2017-12-28 19:21",
#             "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f",
#             "album_id": ""
#         },
#         "album": {
#             "name": "The Lord of The Rings: The Two Towers (Original Motion Picture Soundtrack)",
#             "mbid": "",
#             "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f"
#         }
#     },
#     {
#         "date": "2017-12-28 19:14",
#         "uts_date": "1514488440",
#         "artist": {
#             "name": "Howard Shore",
#             "mbid": "9b58672a-e68e-4972-956e-a8985a165a1f"
#         },
#         "track": {
#             "name": "The Breaking of the Fellowship",
#             "mbid": "",
#             "end_time": "2017-12-28 19:14",
#             "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f",
#             "album_id": ""
#         },
#         "album": {
#             "name": "The Lord of the Rings: The Fellowship of the Ring (Original Motion Picture Soundtrack)",
#             "mbid": "",
#             "artist_id": "9b58672a-e68e-4972-956e-a8985a165a1f"
#         }
#     },
#     {
#         "date": "2017-12-28 19:12",
#         "uts_date": "1514488320",
#         "artist": {
#             "name": "Ramin Djawadi",
#             "mbid": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
#         },
#         "track": {
#             "name": "Main Title",
#             "mbid": "03a20b59-72ea-4806-9518-a481a54ad144",
#             "end_time": "2017-12-28 19:12",
#             "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1",
#             "album_id": ""
#         },
#         "album": {
#             "name": "Game Of Thrones",
#             "mbid": "",
#             "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
#         }
#     },
#     {
#         "date": "2017-12-28 19:10",
#         "uts_date": "1514488200",
#         "artist": {
#             "name": "Ramin Djawadi",
#             "mbid": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
#         },
#         "track": {
#             "name": "Main Title",
#             "mbid": "03a20b59-72ea-4806-9518-a481a54ad144",
#             "end_time": "2017-12-28 19:12",
#             "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1",
#             "album_id": ""
#         },
#         "album": {
#             "name": "Game Of Thrones",
#             "mbid": "",
#             "artist_id": "f089f636-6b85-4e0e-a192-0d30ed2b44d1"
#         }
#     },
#     {
#         "date": "2017-12-28 19:00",
#         "uts_date": "1514487600",
#         "artist": {
#             "name": "Ramin Djawadi",
#             "mbid": ""
#         },
#         "track": {
#             "name": "Main Title",
#             "mbid": "",
#             "end_time": "2017-12-28 19:00",
#             "artist_id": "",
#             "album_id": ""
#         },
#         "album": {
#             "name": "West world",
#             "mbid": "",
#             "artist_id": ""
#         }
#     },
#     {
#         "date": "2017-12-28 18:50",
#         "uts_date": "1514487000",
#         "artist": {
#             "name": "Floppotron covers",
#             "mbid": ""
#         },
#         "track": {
#             "name": "Main Title",
#             "mbid": "",
#             "end_time": "2017-12-28 18:50",
#             "artist_id": "",
#             "album_id": ""
#         },
#         "album": {
#             "name": "West world",
#             "mbid": "",
#             "artist_id": ""
#         }
#     }
# ]
# """
