"""Module for testing the statistics modules
"""
from track_record.postprocess import stat_gen
# import sqlite3 as sql3
# import sqlalchemy as sqlal
import unittest


DB_FILENAME = "test_database.db"


def test_predefined_queries():
    """Tests predefined queries"""
    queries = stat_gen.PREDEFINED_QUERIES
    # print(queries)
    # qs = [queries[k] for k in queries.keys()]
    # print(qs[:4])
    # print(stat_gen.execute_queries(qs[]))

    print("testing query: ", queries["count_total_listens"])
    print(stat_gen.execute_predef_query("count_total_listens", DB_FILENAME))
    stats = stat_gen.get_statistics(DB_FILENAME)
    for stat in stats:
        print("Infotext: {}, result: {}\n ".format(stat[0], stat[1]))


class TestStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        return super().setUpClass()

    def tearDownClass(cls):
        return super().tearDownClass()

    def test_pandas_num_listens():
        # assert
        pass