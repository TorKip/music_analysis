"""Module for testing the statistics modules
"""
from track_record.postprocess import stat_gen


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
