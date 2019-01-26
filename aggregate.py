import json
# import numpy as np
# import matplotlib.pyplot as plt
import visualize
import spot_utils
# import sys


spotify_filename = "music_history/SpotifyTest.json"
lastfm_filename = "music_history/LastFmTest.json"
aggregate_filename = "AggregatedHistory.json"


def create_history(option="all"):
    if option == "spotify":
        history = load_json_history(spotify_filename)
    elif option == "lastfm":
        # history = load_json_history(lastfm_filename)
        pass
    else:   # option should be all
        history = []
        history.extend(load_json_history(spotify_filename))
        # history.append(load_json_history(lastfm_filename))
    aggregated_data = aggregate_history(history)
    # print(aggregated_data["aggregated_dict"][])
    save_json_history(aggregate_filename, aggregated_data)


def load_json_history(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as history_file:
            history = json.load(history_file)
    except IOError as er:
        print(er)
        history = []
    return history


def save_json_history(filename, data):
    try:
        with open(filename, "w", encoding='utf-8') as aggregated_file:
            json.dump(data, aggregated_file, ensure_ascii=False)
    except IOError as er:
        print(er)


def aggregate_history(play_history_list, source="spotify"):
    keys = {
        "spotify": {
            "artist": "artistName",
            "track": "trackName",
            "dateTime": "endTime"},
        "lastFM": {
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
            aggregated_dict[key] = {
                "artistName": artist,
                "trackName": track,
                'endTimeList':
                    [p[time_date_key] if source == "spotify"
                        else spot_utils.parse_date(
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


def get_most_played_song(play_list):
    most_played_song = play_list[0]
    timespan = "."  # get timespan from endTimeList
    stat_entry = {
        'stat_title': 'Most played song',
        'flavour_text':
            "\"{}\" by {} was played {} times{}".format(
                                            most_played_song['trackName'],
                                            most_played_song['artistName'],
                                            most_played_song['timesPlayed'],
                                            timespan),
        'graph': False}
    return stat_entry


def get_hourly_rate(play_list):
    hourly_plays = [0 for x in range(24)]
    for song in play_list:
        for p in song['endTimeList']:
            time = int(p.split()[1].split(':')[0])
            hourly_plays[time] += 1

    stat_entry = {
        'stat_title': 'Plays at time of day',
        'flavour_text':
            'This stat shows at what time of day songs have been played',
        'graph': True,
        'graph_type': 'polar_bar',
        'radial_axis': [x for x in range(24)],
        'data': hourly_plays,
        'radial_label': 'time',
        'data_label': 'plays'
    }
    return stat_entry


def make_stat_dict(list_dict_tuple):
    play_list = list_dict_tuple[0]
    # play_dict = list_dict_tuple[1]
    stat_dict = {}
    stat_dict['Most_played_song'] = get_most_played_song(play_list)
    stat_dict['Hourly_plays'] = get_hourly_rate(play_list)
    return stat_dict


def process_statistics(filename="AggregatedHistory.json"):
    aggregated_history = load_json_history(filename)
    # aggregated_data = aggregate_history(hist_list)
    list_dict_tuple = (
                        aggregated_history['aggregated_list'],
                        aggregated_history['aggregated_dict'])
    stat_dict = make_stat_dict(list_dict_tuple)

    visualize.cool_stat_print(stat_dict)
