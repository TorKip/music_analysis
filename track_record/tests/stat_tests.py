"""Module for testing the statistics modules
"""
from track_record.postprocess import stat_gen
import sqlite3 as sql3
import sqlalchemy as sqlal
import unittest



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
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.db_connection.close()
        return super().tearDownClass()

    def test_pandas_num_listens(self):
        self.assertEqual(True, False)

    def test_pandas_num_tracks(self):
        self.assertEqual(True, False)

    def test_pandas_num_albums(self):
        self.assertEqual(True, False)

    def test_pandas_num_artists(self):
        self.assertEqual(True, False)
        
    def test_pandas_most_listened_artist(self):
        self.assertEqual(True, False)
    
    def test_pandas_most_listened_album(self):
        self.assertEqual(True, False)
    
    def test_pandas_most_listened_track(self):
        self.assertEqual(True, False)

    def test_pandas_timebound_listens(self):
        self.assertEqual(True, False)

    def test_pandas_timebound_result(self):
        self.assertEqual(True, False)

    def test_pandas_listens_per_hour(self):
        self.assertEqual(True, False)

    def test_pandas_result_per_hour(self):
        self.assertEqual(True, False)

    def test_pandas_read_db(self):
        self.assertEqual(True, False)
