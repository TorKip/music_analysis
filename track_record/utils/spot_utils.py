import spotipy
import json
from datetime import datetime
    

def parse_date(datestring):
    """Returns formated date
    
    datestring: datetime with shape: "dd MMM yyyy, hh:mm",
    with shorthand for month eg DEC = december

    return: datetime with shape: "YYYY-MM-DD-hh:mm"
    """
    months = {
        "Dec": "12",
        "Nov": "11",
        "Oct": "10",
        "Sep": "09",
        "Aug": "08",
        "Jul": "07",
        "Jun": "06",
        "May": "05",
        "Apr": "04",
        "Mar": "03",
        "Feb": "02",
        "Jan": "01"
        }
    date = datestring.split()
    year = date[2].strip(",")
    month = months[date[1]]
    day = date[0]
    time = date[3]
    new_date = "{}-{}-{} {}".format(year, month, day, time)
    return new_date


def date_string_to_uts(datestring=None, year=None, month=None,
                       day=None, hour=None, minute=None):
    """ Formats

        Datestring: "YYYY-MM-DD HH:MM"

        year: "YYYY"
        month: "MM"
        day: "DD"
        time: "HH:MM"
    """
    uts_time = 0
    if datestring is not None:
        date_str, time_str = datestring.split()
        year, month, day = date_str.split("-")
        hour, minute = time_str.split(":")
        print(year, month, day, hour, minute)
        dt = datetime(year=int(year), month=int(month), day=int(day),
                      hour=int(hour),
                      minute=int(minute))
        uts_time = int(dt.timestamp())
        
    return uts_time


# spotipy interfacing
def get_spotify_id(trackname="", artist="", album=""):
    """NOT IMPLEMENTED 

    Gets spotify id based on trackname, artist or album
    """
    spotify = spotipy.Spotify()
    # results = spotify.search(q="track:" + trackname, type="track")
    results = spotify.search(q='artist:' + artist, type='artist')
    # results = ""    # Until Spotify api is set up
    return results


# get_spotify_id("Sometimes")
def load_json_history(filename):
    """Loads filename containing json object
    returns json list or [] if read error
    """
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
        with open(filename, "w", encoding='utf-8') as aggregated_file:
            json.dump(data, aggregated_file, indent=4, ensure_ascii=False)
    except IOError as er:
        print(er)


if __name__ == "__main__":
    print(date_string_to_uts("2017-12-13 17:43"))
