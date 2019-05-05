# import numpy as np
import pandas as pd
from track_record.utils import db_tools as dbt
import time


HISTORY_DATABASE = "history.db"


# def load_total_history(history_database=HISTORY_DATABASE):
#     engine = dbt.get_connectable(history_database)

#     listens = pd.read_sql_table("listens", con=engine)
#     tracks = pd.read_sql("tracks", con=engine)
#     # albums = pd.read_sql_table("albums", con=engine)
#     # artists = pd.read_sql_table("artists", con=engine)
#     print(listens.head(7))
#     print(tracks.head(7))
#     lis_tra = pd.merge(listens, tracks, left_on='track_id', right_on='id')

#     print(lis_tra.head(7))


def get_num_listens(db_file=HISTORY_DATABASE):
    """Returns number of listenes in the database"""
    engine = dbt.get_connectable(db_file)
    description = "Total number of listens in dataset"
    num_listens = pd.read_sql_table("listens", con=engine).id.nunique()
    return (description, num_listens)


def get_num_tracks(db_file=HISTORY_DATABASE):
    """Returns number of tracks in the database"""
    engine = dbt.get_connectable(db_file)
    description = "Number of unique tracks in dataset"
    num_tracks = pd.read_sql_table("tracks", con=engine).id.nunique()
    return (description, num_tracks)


def get_num_albums(db_file=HISTORY_DATABASE):
    """Returns number of albums in the database"""
    engine = dbt.get_connectable(db_file)
    description = "Number of unique albums in dataset"
    num_albums = pd.read_sql_table("albums", con=engine).id.nunique()
    return (description, num_albums)


def get_num_artists(db_file=HISTORY_DATABASE):
    """Returns number of artists in the database"""
    engine = dbt.get_connectable(db_file)
    description = "Number of unique artists in dataset"
    num_artists = pd.read_sql_table("artists", con=engine).id.nunique()
    return (description, num_artists)


# def get_most_listened_artists(number_of_artists=1, db_file=HISTORY_DATABASE):
#     top_artists = artists.query("id in @data")[["id", "artist_name", "misc"]]
#     print(data)
#     return(top_artists)

def get_most_listened_artists(number_of_artists=1, db_file=HISTORY_DATABASE,
                              listens=None, artists=None):
    """Returns the most listened to artist(s) as a tuple with description
    and sorted pandas.Dataframe

    result shape:
    (description, pandas.Dataframe)

    Description: The <number_of_artists> most listened to artists in the
    dataset

    Dataframe shape:
    id_x    artist_id   artist_name     count
    int     int         string          int
    ...     ...         ...             ...
    """
    description = "The {} most listened to artists in the dataset"\
        .format(number_of_artists)
    if listens is None or artists is None:    
        engine = dbt.get_connectable(db_file)
    if listens is None:
        listens = pd.read_sql_table("listens", con=engine)
    if artists is None:
        artists = pd.read_sql_table("artists", con=engine)

    count = listens[["id", "artist_id"]].groupby("artist_id").count()\
        .rename(index=int, columns={"id": "count"})

    data = pd.merge(artists[["id", "artist_name"]], count[["count"]],
                    left_on="id", right_on="artist_id")\
        .nlargest(number_of_artists, "count")
 
    return (description, data)


def get_most_listened_albums(number_of_albums=1, db_file=HISTORY_DATABASE,
                             listens=None, albums=None):
    """Returns the most listened to album(s) as a tuple with description
    and sorted pandas.Dataframe

    result shape:
    (description, pandas.Dataframe)

    Description: The <number_of_albums> most listened to albums in the dataset

    Dataframe shape:
    id_x    album_id    album_name      count
    int     int         string          int
    ...     ...         ...             ...
    """
    description = "The {} most listened to albums in the dataset"\
        .format(number_of_albums)
    if listens is None or albums is None:
        engine = dbt.get_connectable(db_file)
    if listens is None:
        listens = pd.read_sql_table("listens", con=engine)
    if albums is None:
        albums = pd.read_sql_table("albums", con=engine)

    count = listens[["id", "album_id"]].groupby("album_id").count()\
        .rename(index=int, columns={"id": "count"})

    data = pd.merge(albums[["id", "album_name"]], count[["count"]],
                    left_on="id", right_on="album_id")\
        .nlargest(number_of_albums, "count")

    return (description, data)


def get_most_listened_tracks(number_of_tracks=1, db_file=HISTORY_DATABASE,
                             listens=None, tracks=None):
    """Returns the most listened to track(s) as a tuple with description
    and sorted pandas.Dataframe

    result shape:
    (description, pandas.Dataframe)

    Description: The <number_of_tracks> most listened to tracks in the dataset

    Dataframe shape:
    index   id          track_name      count
    int     int         string          int
    ...     ...         ...             ...
    """
    description = "The {} most listened to tracks in the dataset"\
        .format(number_of_tracks)
    if listens is None or tracks is None:
        engine = dbt.get_connectable(db_file)
    if listens is None:
        listens = pd.read_sql_table("listens", con=engine)
    if tracks is None:
        tracks = pd.read_sql_table("tracks", con=engine)

    count = listens[["id", "track_id"]].groupby("track_id").count()\
        .rename(index=int, columns={"id": "count"})

    data = pd.merge(tracks[["id", "track_name"]], count[["count"]],
                    left_on="id", right_on="track_id")\
        .nlargest(number_of_tracks, "count")

    return (description, data)


def read_db():
    engine = dbt.get_connectable(HISTORY_DATABASE)
    listens = pd.read_sql_table("listens", con=engine)
    tracks = pd.read_sql_table("tracks", con=engine)
    albums = pd.read_sql_table("albums", con=engine)
    artists = pd.read_sql_table("artists", con=engine)
    return listens, tracks, albums, artists
    

if __name__ == "__main__":
    results = []
    start = time.time()
    results.append(get_num_listens())
    results.append(get_num_tracks())
    results.append(get_num_albums())
    results.append(get_num_artists())
    
    listens = None
    tracks = None
    albums = None
    artists = None
    
    listens, tracks, albums, artists = read_db()

    results.append(get_most_listened_artists(number_of_artists=3,\
                   listens=listens, artists=artists))
    results.append(get_most_listened_albums(number_of_albums=3,\
                   listens=listens, albums=albums))
    results.append(get_most_listened_tracks(number_of_tracks=3,\
                   listens=listens, tracks=tracks))
    stop = time.time()
    for s in results:
        for e in s:
            print(e)
    print(stop-start)
