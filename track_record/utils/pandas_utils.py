"""Module containing methods for pandas processing of data"""
import time
import numpy as np
import pandas as pd
from track_record.utils import db_tools as dbt, spot_utils as spu
from sqlalchemy.exc import InvalidRequestError


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


def get_num_listens(listens=None, db_file=HISTORY_DATABASE):
    """Returns number of listens in the dataframe or database.

    If listens is set db_file will be ignored.
    """
    description = "Total number of listens in dataset"
    if listens is None:
        try:
            engine = dbt.get_connectable(db_file)
            listens = pd.read_sql_table("listens", con=engine)
        except (InvalidRequestError, ValueError) as e:
            description = "Error: {}".format(e) + description
            column_names = ["id", "track_id", "album_id",
                "artist_id", "end_time", "uts_end_time"]
            listens = pd.DataFrame(columns=column_names)
    num_listens = listens.id.nunique()
    return (description, num_listens)


def get_num_tracks(tracks=None, db_file=HISTORY_DATABASE):
    """Returns number of tracks in the dataframe og database.

    If tracks is set db_file will be ignored.
    """
    description = "Number of unique tracks in dataset"
    if tracks is None:
        try:
            engine = dbt.get_connectable(db_file)
            tracks = pd.read_sql_table("tracks", con=engine)
        except (InvalidRequestError, ValueError) as e:
            description = "Error: {}".format(e) + description
            column_names = ["id", "track_name", "mbid",
                "spid", "album_id"]
            tracks = pd.DataFrame(columns=column_names)
    num_tracks = tracks.id.nunique()
    return (description, num_tracks)


def get_num_albums(albums=None, db_file=HISTORY_DATABASE):
    """Returns number of albums in the dataframe or database.

    If albums is set db_file will be ignored.
    """
    description = "Number of unique albums in dataset"
    if albums is None:
        try:
            engine = dbt.get_connectable(db_file)
            albums = pd.read_sql_table("albums", con=engine)
        except (InvalidRequestError, ValueError) as e:
            description = "Error: {}".format(e) + description
            column_names = ["id", "album_name", "mbid",
                "spid", "artist_id"]
            albums = pd.DataFrame(columns=column_names)
    num_albums = albums.id.nunique()
    return (description, num_albums)


def get_num_artists(artists=None, db_file=HISTORY_DATABASE):
    """Returns number of artists in the dataframe or database.

    If artists is set db_file will be ignored.
    """
    description = "Number of unique artists in dataset"
    if artists is None:
        try:
            engine = dbt.get_connectable(db_file)
            artists = pd.read_sql_table("artists", con=engine)
        except (InvalidRequestError, ValueError) as e:
            description = "Error: {}".format(e) + description
            column_names = ["id", "artist_name", "mbid",
                "spid", "misc"]
            artists = pd.DataFrame(columns=column_names)
    num_artists = artists.id.nunique()
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


def get_timebound_listens(original_listens, start_time=0, end_time=None):
    # print("start time type: {}\n end time type: {}".format(type(start_time),
    #  type(end_time)))
    """Returns a subset of the original listens that have
    uts timestamps between start_time and end_time
    """
    listens = original_listens.copy()
    if end_time is None:
        result = listens[(listens["uts_end_time"] >= start_time)]
    else:
        result = listens[(listens["uts_end_time"] >= start_time)
                         & (listens["uts_end_time"] <= end_time)]
    return result


def get_listens_bound_result(other, listens):
    """Returns a subset of the original tracks, albums or artists based on
    a list of listens.

    """
    name = other.keys()[1]
    
    if name == "track_name":
        ids = listens.track_id
        result = other.query("id in @ids")
    elif name == "album_name":
        ids = listens.album_id
        result = other.query("id in @ids")
    elif name == "artist_name":
        ids = listens.artist_id
        result = other.query("id in @ids")
    else:
        result = other
    return result


def get_listens_per_hour(listens):
    """Returns a np.array of 24 dataframes, each containing listens for respective hour
    result[0] = listens between 00:00-00:59
    result[23] = listens between 23:00-23:59
    """
    results = []
    listens_with_hour = get_hour_of_listens(listens)
    for i in range(24):
        results.append(listens_with_hour[listens_with_hour.hour == i])
    #   TODO
    return results


def get_hour_of_listens(listens):
    """Returns hour of listen for given listen(s) as new dataframe with "hour" column
    hour = 0 to 23
    representing 00:00-00:59 to 23:00-23:59
    """
    #   TODO
    # result = (listen, spu.uts_to_integer_hour(listen.uts_end_time))
    listens = listens.copy()
    listens["hour"] = spu.datestring_to_integer_hour(listens.end_time)
    return listens


def count_occurences_per_hour(occurences_per_hour):
    """Returns list of tuples of shape (int(hour), int(amount_of_listens))

    :listens_per_hour: should be a list of 24 dataframes,
    with index determining what hour it belongs to (0-23)
    """
    result = [(i, int(occurences_per_hour[i].count(axis=0)[["id"]])) 
              for i in range(23)]
    return result


# def count_listens_per_hour_groupby(listens_with_hour):
#     """Returns list of tuples of shape (int(hour), int(amount_of_listens))

#     :listens_per_hour: should be a dataframe with listens containing "hour"
#     column
#     """
#     result = [(i, None) for i in range(24)]
#     count = listens_with_hour.groupby("hour").count()
#     # print(count)
#     return result


def read_db(db_path=HISTORY_DATABASE):
    engine = dbt.get_connectable(db_path)
    listens = pd.read_sql_table("listens", con=engine)
    tracks = pd.read_sql_table("tracks", con=engine)
    albums = pd.read_sql_table("albums", con=engine)
    artists = pd.read_sql_table("artists", con=engine)
    return listens, tracks, albums, artists


# if __name__ == "__main__":
#     # For testing and researching purposes
#     results = []
#     start = time.time()
#     results.append(get_num_listens())
#     results.append(get_num_tracks())
#     results.append(get_num_albums())
#     results.append(get_num_artists())

#     # Initialize and read in standard values from database
#     listens = None
#     tracks = None
#     albums = None
#     artists = None
#     listens, tracks, albums, artists = read_db()

#     # Test 
#     results.append(("hour of listen of{}".format(listens),
#                     get_hour_of_listens(listens)))

#     listens_per_hour = get_listens_per_hour(listens)
#     results.append(listens_per_hour)
#     # start_check = time.time()
#     artists_per_hour = get_num_albums()
#     results.append(("amount of listens per hour is:",
#                     count_occurences_per_hour(listens_per_hour)))
#     # print("time for count_listens_per_hour is {:f}".format(time.time()-start_check))
#     # start_check = time.time()
#     # results.append(("amount of listens per hour is",
#     #                 count_listens_per_hour_groupby(get_hour_of_listens(listens))))
#     # print("time for count_listens_per_hour_groupby is {:f}".format(time.time()-start_check))
#     start_date = spu.date_string_to_uts("2017-05-17 01:00")
#     end_date = spu.date_string_to_uts("2017-05-18 23:00")

#     listens = get_timebound_listens(listens, start_date, end_date)
#     # results.append(("listens\n", listens))


#     # results.append(("", listens))
#     # results.append(get_most_listened_artists(number_of_artists=3,
#     #                listens=listens, artists=artists))
#     # results.append(get_most_listened_albums(number_of_albums=3,
#     #                listens=listens, albums=albums))
#     # results.append(get_most_listened_tracks(number_of_tracks=3,
#     #                listens=listens, tracks=tracks))
#     # results.append(("tracks:\n", get_listens_bound_result(tracks,
#     #     listens=listens)))
#     # results.append(("albums:\n", get_listens_bound_result(albums,
#     #     listens=listens)))
#     # results.append(("artists:\n",get_listens_bound_result(artists,
#     #     listens=listens)))
#     # results.append((listens.head(5), type(listens),
#     #  listens["uts_end_time"].dtype))
#     # results.append(("all listens: 0 - float(inf)",
#     #                 get_timebound_listens(listens).head()))
#     # results.append(("listens from: 1514409713 - 1514410980",
#     #      get_timebound_listens(listens, start_time=1511203836,
#     #                            end_time=1513697746).head()))
#     # start_date = spu.date_string_to_uts("2017-05-17 22:00")
#     # end_date = spu.date_string_to_uts("2017-05-23 15:00")

#     stop = time.time()
#     for s in results:
#         for e in s:
#             # print(e)
#             pass
#     print(stop-start)
