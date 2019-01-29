import spotipy
import json
    

def parse_date(datestring):
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

# spotipy interfacing
def get_spotify_id(trackname="", artist="", album=""):
    # spotify = spotipy.Spotify()
    # results = spotify.search(q="track:" + trackname, type="track")
    results = ""    # Until Spotify api is set up
    return results

# get_spotify_id("Sometimes")
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
            json.dump(data, aggregated_file, indent=4, ensure_ascii=False)
    except IOError as er:
        print(er)
