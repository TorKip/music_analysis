import sqlite3
import contextlib
from track_record.utils import db_tools

predefined_queries = {
    "count_total_listens": (""" SELECT COUNT(*) FROM listens""", "Totals listens in history"),
    "count_total_tracks": (""" SELECT COUNT(*) FROM tracks""", "Total amount of tracks registered in history"),
    "count_total_albums": (""" SELECT COUNT(*) FROM albums""", "Total amount of albums registered in history"),
    "count_total_artists": (""" SELECT COUNT(*) FROM artists""", "Total amount of artists registered in history"),
    "most_listened_track": (""" SELECT COUNT(*), track_name FROM listens 
            JOIN tracks ON listens.track_id = tracks.id
            GROUP BY track_id ORDER BY COUNT(*) DESC LIMIT 1
            """,
            "Most listened to track"),
    "most_listened_album": ("""SELECT COUNT(*), album_name from listens 
            JOIN tracks ON listens.track_id = tracks.id 
            JOIN albums ON tracks.album_id = albums.id 
            GROUP BY album_id ORDER BY COUNT(*) DESC LIMIT 1
            """,
            "Most listened to album"),
    "most_listened_artist": ("""SELECT COUNT(*), artist_name from listens
            JOIN tracks on listens.track_id = tracks.id
            JOIN albums on tracks.album_id = albums.id
            JOIN artists on albums.artist_id = artists.id
            GROUP BY artist_id ORDER BY COUNT(*) DESC LIMIT 1
            """, "Most listened to artist")
}

def execute_queries(q_args=[], history_db_filepath="history.db"):
    """Takes a list of queries and returns the result in a list

    q_args -- list of queries with shape: (sql, info_text)

    Keyword arguments: \n
    history_db_filepath -- history database path (default: history.db)
    """
    if not q_args:
        return "No queries given"
    else:
        results = []
        for q in q_args:
            try:
                results.append((q[1], db_tools.execute_static_query(db_filepath=history_db_filepath, sql=q[0])))
            except sqlite3.Error as e:
                results.append((q[1], "Invalid query"))
    return results

def execute_predef_query(query_id, history_db_filepath="history.db"):
    """Executes a query from predefined_queries"""
    try:
        sql = predefined_queries[query_id]
    except KeyError as e:
        return ("No predefined query exists for", query_id)
    try:
        result = db_tools.execute_static_query(db_filepath=history_db_filepath, sql=sql[0])
        return result
    except sqlite3.Error as e:
        return (sql[1], "Invalid query")
        
        

def get_statistics(history_db_filepath="history.db"):
    """Executes a series of queries and returns the result as a list"""
    queries = [predefined_queries[k] for k in predefined_queries.keys()]
    results = execute_queries(q_args=queries, history_db_filepath=history_db_filepath)
    return results





# def count_total_listens(history_db_filepath="history.db"):
#     sql = predefined_queries["count_total_listens"]
#     count = execute_queries(sql, history_db_filepath=history_db_filepath)[0]
#     return count

# def count_total_tracks(history_db_filepath="history.db"):
#     sql = """ SELECT COUNT(*) FROM tracks"""
#     count = [0]
#     return count

# def count_total_albums(history_db_filepath="history.db"):
#     sql = """ SELECT COUNT(*) FROM albums"""
#     count = db_tools.execute_static_query(history_db_filepath, sql)[0][0]
#     return count

# def count_total_artists(history_db_filepath="history.db"):
#     sql = """ SELECT COUNT(*) FROM artists"""
#     count = db_tools.execute_static_query(history_db_filepath,sql)[0][0]
#     return count

# def get_most_listened_track(history_db_filepath="history.db"):
#     sql = """ SELECT COUNT(*), track_name FROM listens 
#             JOIN tracks ON listens.track_id = tracks.id
#             GROUP BY track_id ORDER BY COUNT(*) DESC
#             """
#     result = db_tools.execute_static_query(history_db_filepath, sql)[0]
#     return result

# def get_most_listened_album(history_db_filepath="history.db"):
#     sql = """SELECT COUNT(*), album_name from listens 
#             JOIN tracks ON listens.track_id = tracks.id 
#             JOIN albums ON tracks.album_id = albums.id 
#             GROUP BY album_id ORDER BY COUNT(*) DESC
#             """
#     result = db_tools.execute_static_query(history_db_filepath, sql)[0]
#     return result

# def get_most_listened_artist(history_db_filepath="history.db"):
#     sql = """SELECT COUNT(*), artist_name from listens
#             JOIN tracks on listens.track_id = tracks.id
#             JOIN albums on tracks.album_id = albums.id
#             JOIN artists on albums.artist_id = artists.id
#             GROUP BY artist_id ORDER BY COUNT(*) DESC
#             """
#     result = db_tools.execute_static_query(history_db_filepath, sql)[0]
#     return result
