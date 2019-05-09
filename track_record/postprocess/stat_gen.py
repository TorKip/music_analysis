"""Module containing methods for generating statistics
"""
import sqlite3
# import contextlib
from track_record.utils import db_tools, pandas_utils

PREDEFINED_QUERIES = {
    "count_total_listens": (""" SELECT COUNT(*) FROM listens""",
                            "Totals listens in history"),
    "count_total_tracks": (""" SELECT COUNT(*) FROM tracks""",
                           "Total amount of tracks registered in history"),
    "count_total_albums": (""" SELECT COUNT(*) FROM albums""",
                           "Total amount of albums registered in history"),
    "count_total_artists": (""" SELECT COUNT(*) FROM artists""",
                            "Total amount of artists registered in history"),
    "most_listened_track": (""" SELECT COUNT(*), track_name FROM listens
                            JOIN tracks ON listens.track_id = tracks.id
                            GROUP BY track_id ORDER BY COUNT(*) DESC LIMIT 1
                            """,
                            "Most listened to track"),
    "most_listened_album": ("""SELECT COUNT(*), album_name from listens
                            JOIN albums ON listens.album_id = albums.id
                            GROUP BY album_id ORDER BY COUNT(*) DESC LIMIT 1
                            """,
                            "Most listened to album"),
    "most_listened_artist": ("""SELECT COUNT(*), artist_name from listens
                             JOIN artists on listens.artist_id = artists.id
                             GROUP BY artist_id ORDER BY COUNT(*) DESC LIMIT 1
                             """,
                             "Most listened to artist")
}


def execute_queries(q_args, history_db_filepath="history.db"):
    """Takes a list of queries and returns the result in a list

    q_args -- list of queries with shape: (sql, info_text)

    Keyword arguments: \n
    history_db_filepath -- history database path (default: history.db)
    """
    if not q_args:
        return "No queries given"
    else:
        results = []
        for queries in q_args:
            try:
                results.append((queries[1], db_tools.execute_static_query(
                    db_filepath=history_db_filepath, sql=queries[0])))
            except sqlite3.Error:
                results.append((queries[1], "Invalid query"))
    return results


def execute_predef_query(query_id, history_db_filepath="history.db"):
    """Executes a query from PREDEFINED_QUERIES"""
    try:
        sql = PREDEFINED_QUERIES[query_id]
    except KeyError:
        return ("No predefined query exists for", query_id)
    try:
        result = db_tools.execute_static_query(db_filepath=history_db_filepath,
                                               sql=sql[0])
        return result
    except sqlite3.Error:
        return (sql[1], "Invalid query")


def get_statistics(history_db_filepath="history.db"):
    """Executes a series of queries and returns the result as a list"""
    # queries = [PREDEFINED_QUERIES[k] for k in PREDEFINED_QUERIES.keys()]
    # results = execute_queries(q_args=queries,
    #               history_db_filepath=history_db_filepath)
    history_db = history_db_filepath  # random use to prevent lint-error
    history_db.lower()
    results = []
    results.append(pandas_utils.get_num_listens())
    results.append(pandas_utils.get_num_tracks())
    results.append(pandas_utils.get_num_albums())
    results.append(pandas_utils.get_num_artists())
    results.append(pandas_utils.get_most_listened_tracks(3))
    results.append(pandas_utils.get_most_listened_albums(3))
    results.append(pandas_utils.get_most_listened_artists(3))
    return results
