import json
# import numpy as np
# import matplotlib.pyplot as plt
import track_record.postprocess.visualize as visualize
from track_record.utils.spot_utils import parse_date, get_spotify_id
import track_record.postprocess.stat_gen as stat_gen
# import sys


spotify_filename = "track_record/music_history/SpotifyTest.json"
lastfm_filename = "track_record/music_history/LastFmTest.json"
aggregate_filename = "track_record/music_history/AggregatedHistory.json"


def create_history(option="all"):
    """DEPRECATED Creates a history dict based on source
    
    Source: spotify or lastfm
    """
    if option == "spotify":
        history = load_json_history(spotify_filename)
    elif option == "lastfm":
        history = load_json_history(lastfm_filename)
    else:   # option should be all
        history = []
        history.extend(load_json_history(spotify_filename))
        # history.append(load_json_history(lastfm_filename))
    aggregated_data = aggregate_history(history, option)
    # print(aggregated_data["aggregated_dict"][])
    save_json_history(aggregate_filename, aggregated_data)


def load_json_history(filename):
    """Loads given path as json dict and returns result or []"""
    try:
        with open(filename, 'r', encoding='utf-8') as history_file:
            history = json.load(history_file)
    except IOError as er:
        print(er)
        history = []
    return history


def save_json_history(filename, data):
    """Saves json data to path filename"""
    try:
        with open(filename, "w+", encoding='utf-8') as aggregated_file:
            json.dump(data, aggregated_file, indent=4, ensure_ascii=False)
    except IOError as er:
        print(er)


def aggregate_history(play_history_list, source="spotify"):
    """DEPRECATED Takes a list of plays and aggregates them into different statistics"""
    print("aggregating history from source: {}".format(source))
    keys = {
        "spotify": {
            "artist": "artistName",
            "track": "trackName",
            "dateTime": "endTime"},
        "lastfm": {
            "artist": "artist",
            "track": "name",
            "dateTime": "date"}
        }

    aggreagated_list = []
    artist_key = keys[source]["artist"]
    track_key = keys[source]["track"]
    time_date_key = keys[source]["dateTime"]

    aggregated_dict = {}

    for p in play_history_list:
        artist = p[artist_key] if source == "spotify"\
                    else p[artist_key]["#text"]
        track = p[track_key] if source == "spotify" else p[track_key]
        key = "{}###{}".format(artist, track)
        if key not in aggregated_dict.keys():
            spotify_id = get_spotify_id(trackname=track, artist=artist)
            aggregated_dict[key] = {
                "spotifyId": spotify_id,
                "artistName": artist,
                "trackName": track,
                'endTimeList':
                    [p[time_date_key] if source == "spotify"
                        else parse_date(
                            p[time_date_key]["#text"])],
                'timesPlayed': 1
                }
        elif key in aggregated_dict.keys():
            aggregated_dict[key]['endTimeList'].append(p[time_date_key])
            aggregated_dict[key]['timesPlayed'] += 1
        else:
            print('Something went wrong!\nKey not in dict nor not in dict?')

    for ad_p in aggregated_dict.keys():
        aggreagated_list.append(aggregated_dict[ad_p])

    aggreagated_list.sort(
        key=lambda dictionary:
        dictionary['timesPlayed'],
        reverse=True)
    meta_dict = {}
    data = {
        'aggregated_list': aggreagated_list,
        'aggregated_dict': aggregated_dict,
        'meta_dict': meta_dict}
    return data


def get_most_played_track(play_list):
    """DEPRECATED Gets most played track from list of plays"""
    most_played_track = play_list[0]
    timespan = "."  # get timespan from endTimeList
    stat_entry = {
        'stat_title': 'Most played track',
        'flavour_text':
            "\"{}\" by {} was played {} times{}".format(
                                            most_played_track['trackName'],
                                            most_played_track['artistName'],
                                            most_played_track['timesPlayed'],
                                            timespan),
        'graph': False}
    return stat_entry


def get_hourly_rate(play_list):
    """Returns amount of plays for each hour of the day"""
    hourly_plays = [0 for x in range(24)]
    for track in play_list:
        for p in track['endTimeList']:
            time = int(p.split()[1].split(':')[0])
            hourly_plays[time] += 1

    stat_entry = {
        'stat_title': 'Plays at time of day',
        'flavour_text':
            'This stat shows at what time of day tracks have been played',
        'graph': True,
        'graph_type': 'polar_bar',
        'radial_axis': [x for x in range(24)],
        'data': hourly_plays,
        'radial_label': 'time',
        'data_label': 'plays'
    }
    return stat_entry


def make_stat_dict(list_dict_tuple):
    """Compiles a dictionary of statistics given a (list, dict) tuple"""
    play_list = list_dict_tuple[0]
    # play_dict = list_dict_tuple[1]
    stat_dict = {}
    stat_dict['Most_played_track'] = get_most_played_track(play_list)
    stat_dict['Hourly_plays'] = get_hourly_rate(play_list)
    return stat_dict


def process_statistics(filename="AggregatedHistory.json"):
    """Compiles statistics from aggregated history"""
    aggregated_history = load_json_history(filename)
    # aggregated_data = aggregate_history(hist_list)
    list_dict_tuple = (
                        aggregated_history['aggregated_list'],
                        aggregated_history['aggregated_dict'])
    stat_dict = make_stat_dict(list_dict_tuple)

    visualize.cool_stat_print(stat_dict)
