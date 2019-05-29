"""Module for testing the statistics modules
"""
import unittest
import sqlite3 as sql3
import sqlalchemy as sqlal
import pandas as pd
from track_record.postprocess import stat_gen
from track_record.utils import db_tools
from track_record.utils import pandas_utils as pdut



# DB_FILENAME = "test_database.db"


# def test_predefined_queries():
#     """Tests predefined queries"""
#     queries = stat_gen.PREDEFINED_QUERIES
#     # print(queries)
#     # qs = [queries[k] for k in queries.keys()]
#     # print(qs[:4])
#     # print(stat_gen.execute_queries(qs[]))

#     print("testing query: ", queries["count_total_listens"])
#     print(stat_gen.execute_predef_query("count_total_listens", DB_FILENAME))
#     stats = stat_gen.get_statistics(DB_FILENAME)
#     for stat in stats:
#         print("Infotext: {}, result: {}\n ".format(stat[0], stat[1]))
def statistics_test_suite():
    load_testCase = unittest.TestLoader.loadTestsFromTestCase
    test_loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTest(load_testCase(test_loader, TestStatistics))
    return suite


class TestStatistics(unittest.TestCase):
    database_name = "track_record/tests/static_test_database.db"
    @classmethod
    def setUpClass(cls):
        cls.db_connection = sql3.connect(cls.database_name)
        cls.db_cursor = cls.db_connection.cursor()
        cls.engine = db_tools.get_connectable(cls.database_name)
        cls.listens = pd.read_sql_table("listens", con=cls.engine)
        cls.tracks = pd.read_sql_table("tracks", con=cls.engine)
        cls.albums = pd.read_sql_table("albums", con=cls.engine)
        cls.artists = pd.read_sql_table("artists", con=cls.engine)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.db_connection.close()
        return super().tearDownClass()
    
    # def test_pandas_read_db(self):
    #     listens, tracks, albums, artists = pdut.read_db(self.database_name)
    #     # print(listens)
    #     # print(self.listens)
    #     self.assertEqual(pd.empty)
    #     self.assertEqual(tracks, self.tracks)
    #     self.assertEqual(albums, self.albums)
    #     self.assertEqual(artists, self.artists)
    
    def test_pandas_num_listens(self):
        self.assertEqual(pdut.get_num_listens(
            listens=self.listens)[1], 15)
        self.assertEqual(pdut.get_num_listens(
            db_file=self.database_name)[1], 15)
        self.assertNotEqual(pdut.get_num_listens()[1], 15)
        # self.assertEqual(True, False)

    def test_pandas_num_tracks(self):
        self.assertEqual(pdut.get_num_tracks(tracks=self.tracks)[1], 13)
        self.assertEqual(
            pdut.get_num_tracks(db_file=self.database_name)[1], 13)
        # self.assertEqual(True, False)

    def test_pandas_num_albums(self):
        self.assertEqual(pdut.get_num_albums(albums=self.albums)[1], 11)
        self.assertEqual(
            pdut.get_num_albums(db_file=self.database_name)[1], 11)
        # self.assertEqual(True, False)

    def test_pandas_num_artists(self):
        self.assertEqual(pdut.get_num_artists(artists=self.artists)[1], 8)
        self.assertEqual(
            pdut.get_num_artists(db_file=self.database_name)[1], 8)
        # self.assertEqual(True, False)
        
    def test_pandas_most_listened_artist(self):
        # print(pdut.get_most_listened_artists(2,
        #     db_file=self.database_name)[1])
        self.assertEqual(pdut.get_most_listened_artists(
                db_file=self.database_name)[1].iat[0, 0],
                4)
        self.assertEqual(pdut.get_most_listened_artists(
                2, db_file=self.database_name)[1].iloc[:, 0].tolist(),
                [4, 3])

        self.assertEqual(pdut.get_most_listened_artists(
                2, db_file=self.database_name, listens=self.listens)
                    [1].iloc[:, 0].tolist(),
                    [4, 3])
        self.assertEqual(pdut.get_most_listened_artists(
                2, db_file=self.database_name, artists=self.artists)
                    [1].iloc[:, 0].tolist(),
                    [4, 3])
        self.assertEqual(pdut.get_most_listened_artists(
                2, db_file=self.database_name, listens=self.listens,
                artists=self.artists)[1].iloc[:, 0].tolist(),
                [4, 3])
        self.assertEqual(pdut.get_most_listened_artists(
                2, listens=self.listens, artists=self.artists)
                    [1].iloc[:, 0].tolist(),
                    [4, 3])
            
        # self.assert
        # self.assertEqual(True, False)
    
    def test_pandas_most_listened_album(self):
        self.assertEqual(pdut.get_most_listened_albums(
                db_file=self.database_name)[1].iat[0, 0],
                7)
        self.assertEqual(pdut.get_most_listened_albums(
                2, db_file=self.database_name)[1].iloc[:, 0].tolist(),
                [7, 4])

        self.assertEqual(pdut.get_most_listened_albums(
                2, db_file=self.database_name, listens=self.listens)
                    [1].iloc[:, 0].tolist(),
                    [7, 4])
        self.assertEqual(pdut.get_most_listened_albums(
                2, db_file=self.database_name, albums=self.albums)
                    [1].iloc[:, 0].tolist(),
                    [7, 4])
        self.assertEqual(pdut.get_most_listened_albums(
                2, db_file=self.database_name, listens=self.listens,
                albums=self.albums)[1].iloc[:, 0].tolist(),
                [7, 4])
        self.assertEqual(pdut.get_most_listened_albums(
                2, listens=self.listens, albums=self.albums)
                    [1].iloc[:, 0].tolist(),
                    [7, 4])
        # print(pdut.get_most_listened_albums(2,
        #     db_file=self.database_name)[1])
        #top 2 albums [7,4]
        # self.assertEqual(True, False)
    
    def test_pandas_most_listened_track(self):
        # print(pdut.get_most_listened_tracks(2,
        #     db_file=self.database_name)[1])
        top_2_tracks = [6, 7]
        self.assertEqual(pdut.get_most_listened_tracks(
                db_file=self.database_name)[1].iat[0, 0],
                top_2_tracks[0])
        self.assertEqual(pdut.get_most_listened_tracks(
                2, db_file=self.database_name)[1].iloc[:, 0].tolist(),
                top_2_tracks)

        self.assertEqual(pdut.get_most_listened_tracks(
                2, db_file=self.database_name, listens=self.listens)
                    [1].iloc[:, 0].tolist(),
                    top_2_tracks)
        self.assertEqual(pdut.get_most_listened_tracks(
                2, db_file=self.database_name, tracks=self.tracks)
                    [1].iloc[:, 0].tolist(),
                    top_2_tracks)
        self.assertEqual(pdut.get_most_listened_tracks(
                2, db_file=self.database_name, listens=self.listens,
                tracks=self.tracks)[1].iloc[:, 0].tolist(),
                top_2_tracks)
        self.assertEqual(pdut.get_most_listened_tracks(
                2, listens=self.listens, tracks=self.tracks)
                    [1].iloc[:, 0].tolist(),
                    top_2_tracks)
        # self.assertEqual(True, False)

    def test_pandas_timebound_listens(self):
        # self.assertEqual(True, False)
        end_time = 1514488139
        start_time = 1505918555
        # print(self.listens)
        list_of_listens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        list_of_timebound_listens = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.assertEqual(pdut.get_timebound_listens(self.listens)
            .iloc[:, 0].tolist(),
            list_of_listens)
        self.assertEqual(pdut.get_timebound_listens(
            self.listens, start_time=start_time).iloc[:, 0].tolist(),
            list_of_listens)
        self.assertEqual(pdut.get_timebound_listens(
            self.listens, start_time=start_time, end_time=end_time)
            .iloc[:, 0].tolist(),
            list_of_timebound_listens)

    def test_pandas_timebound_listens_bound_result(self):
        # self.assertEqual(True, False)
        end_time = 1514488139
        start_time = 1505918555
        timebound_listens = pdut.get_timebound_listens(
            self.listens, start_time=start_time, end_time=end_time)
        list_of_listens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        LIST_OF_TIMEBOUND_TRACKS = [6, 7, 8, 9, 10, 11, 12, 13]
        LIST_OF_TIMEBOUND_ALBUMS = [4, 6, 7, 8, 9, 10, 11]
        LIST_OF_TIMEBOUND_ARTISTS = [2, 3, 4, 5, 6, 7, 8]
        # print(timebound_listens)
        # print(pdut.get_listens_bound_result(
        #     self.tracks, timebound_listens))
        self.assertEqual(pdut.get_listens_bound_result(
            self.tracks, timebound_listens).iloc[:, 0].tolist(),
            LIST_OF_TIMEBOUND_TRACKS)
        self.assertEqual(pdut.get_listens_bound_result(
            self.albums, timebound_listens).iloc[:, 0].tolist(),
            LIST_OF_TIMEBOUND_ALBUMS)
        self.assertEqual(pdut.get_listens_bound_result(
            self.artists, timebound_listens).iloc[:, 0].tolist(),
            LIST_OF_TIMEBOUND_ARTISTS)
        self.assertEqual(pdut.get_listens_bound_result(
            self.listens, timebound_listens).iloc[:, 0].tolist(),
            list_of_listens)

    # def test_pandas_listens_per_hour(self):
        # self.assertEqual(True, False)


    # def test_pandas_result_per_hour(self):
    #     self.assertEqual(True, False)

