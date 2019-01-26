from spot_utils import load_json_history, save_json_history, parse_date

SPOTIFY_FILENAME = "music_history/SpotifyTest.json"
# LASTFM_FILENAME = "music_history/LastFmTest.json"
LASTFM_FILENAME = "C:/Users/Tor/Jottacloud/Egne prosjekter/Persondata/Musikkanalyse/lastfmdata/2017.json"
CLEANED_FILENAME = "music_history/cleanlfm.json"
def clean_lfm_data(lfm_history):
    clean_history = []
    
    for entry in lfm_history:
        clean_entry = {}
        artist = entry["artist"]
        album = entry["album"]

        clean_entry["date"] = parse_date(entry["date"]["#text"])
        clean_entry["artist"] = {
            "name":artist["#text"],
            "mbid":artist["mbid"]
        }
        clean_entry["song"] = {
            "name": entry["name"],
            "mbid": entry["mbid"],
            "end_time": clean_entry["date"],
            "artist_id": artist["mbid"],
            "album_id": album["mbid"]
        }
        clean_entry["album"] = {
            "name": album["#text"],
            "mbid": album["mbid"],
            "artist_id": artist["mbid"]
        }
        clean_history.append(clean_entry)
    return clean_history
        
def save_clean_data(option="lastFm"):
    if option == "lastfm":
        data = load_json_history(LASTFM_FILENAME)
        cleaned_data = clean_lfm_data(data)
        save_json_history(CLEANED_FILENAME, cleaned_data)



