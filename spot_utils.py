import spotipy


def parse_date(datestring):
    months = {
        "Dec": "12",
        "Nov": "11",
        "Okt": "10",
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
