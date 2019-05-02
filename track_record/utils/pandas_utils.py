import numpy as np
import pandas as pd
from track_record.utils import db_tools as dbt
# import time


HISTORY_DATABASE = "history.db"


def load_total_history(history_database=HISTORY_DATABASE):
    engine = dbt.get_connectable(history_database)

    listens = pd.read_sql_table("listens", con=engine)
    tracks = pd.read_sql("tracks", con=engine)
    # albums = pd.read_sql_table("albums", con=engine)
    # artists = pd.read_sql_table("artists", con=engine)
    print(listens.head(7))
    print(tracks.head(7))
    lis_tra = pd.merge(listens, tracks, left_on='track_id', right_on='id')
    # lis_tra = listens.join(tracks, on="track_id", how='right', lsuffix="_lis"
    # , rsuffix="_tra")
    # lis_tra_alb_art = listens
    # tra_lis = tracks.join(listens, on="id", lsuffix="_tra", rsuffix="_lis")
    print(lis_tra.head(7))
    # print(list_tra_alb_art.head(7))


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

def get_most_listened_artists(number_of_artists=1, db_file=HISTORY_DATABASE):
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
    engine = dbt.get_connectable(db_file)
    listens = pd.read_sql_table("listens", con=engine)
    artists = pd.read_sql_table("artists", con=engine)
    data = pd.merge(listens, artists, left_on="artist_id", right_on="id")[[
        "id_x", "artist_id", "artist_name"]]
    count = data.groupby("artist_id").id_x.nunique()

    def add_count(x):
        x["count"] = count[x["artist_id"]]
        return x

    data = data.apply(add_count, axis=1).nlargest(number_of_artists, "count")
    return (description, data)


def get_most_listened_albums(number_of_albums=1, db_file=HISTORY_DATABASE):
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
    engine = dbt.get_connectable(db_file)
    listens = pd.read_sql_table("listens", con=engine)
    albums = pd.read_sql_table("albums", con=engine)
    data = pd.merge(listens, albums, left_on="album_id", right_on="id")[[
        "id_x", "album_id", "album_name"]]
    count = data.groupby("album_id").id_x.nunique()

    def add_count(x):
        x["count"] = count[x["album_id"]]
        return x

    data = data.apply(add_count, axis=1).nlargest(number_of_albums, "count")
    return (description, data)


def get_most_listened_tracks(number_of_tracks=1, db_file=HISTORY_DATABASE):
    """Returns the most listened to track(s) as a tuple with description
    and sorted pandas.Dataframe

    result shape:
    (description, pandas.Dataframe)

    Description: The <number_of_tracks> most listened to tracks in the dataset

    Dataframe shape:
    id_x    track_id    track_name      count
    int     int         string          int
    ...     ...         ...             ...
    """
    description = "The {} most listened to tracks in the dataset"\
        .format(number_of_tracks)
    engine = dbt.get_connectable(db_file)
    listens = pd.read_sql_table("listens", con=engine)
    tracks = pd.read_sql_table("tracks", con=engine)
    data = pd.merge(listens, tracks, left_on="track_id", right_on="id")[[
        "id_x", "track_id", "track_name"]]
    count = data.groupby("track_id").id_x.nunique()

    def add_count(x):
        x["count"] = count[x["track_id"]]
        return x

    data = data.apply(add_count, axis=1).nlargest(number_of_tracks, "count")
    return (description, data)

# if __name__ == "__main__":
#     # load_total_history()
#     print(get_num_listens())
#     print(get_num_tracks())
#     print(get_num_albums())
#     print(get_num_artists())
#     print(get_most_listened_artists(number_of_artists=3))
#     print(get_most_listened_albums(number_of_albums=3))
#     print(get_most_listened_tracks(number_of_tracks=3))
