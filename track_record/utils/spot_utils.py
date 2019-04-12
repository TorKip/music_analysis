import spotipy
import json
    

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
