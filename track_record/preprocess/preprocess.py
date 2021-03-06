from track_record.utils.spot_utils import load_json_history
from track_record.utils.spot_utils import save_json_history
from track_record.utils.spot_utils import parse_date
import track_record.utils.db_tools as db

SPOTIFY_FILENAME = "track_record/music_history/SpotifyTest.json"
# LASTFM_FILENAME = "track_record/music_history/LastFmTest.json"
LASTFM_FILENAME = "track_record/music_history/2017.json"
CLEANED_FILENAME = "track_record/music_history/cleanlfm.json"
# DB_FILENAME = "trackrecord/music_history/history.db"
DB_FILENAME = "history.db"


def clean_lfm_data(lfm_history):
    """Creates a clean version of lastFM data"""

    clean_history = []
    try:
        for entry in lfm_history:
            clean_entry = {}
            artist = entry["artist"]
            album = entry["album"]

            clean_entry["date"] = parse_date(entry["date"]["#text"])
            clean_entry["uts_date"] = entry["date"]["uts"]
            clean_entry["artist"] = {
                "name": artist["#text"],
                "mbid": artist["mbid"]
            }
            clean_entry["track"] = {
                "name": entry["name"],
                "mbid": entry["mbid"],
                # "end_time": clean_entry["date"],
                "artist_id": artist["mbid"],
                "album_id": album["mbid"]
            }
            clean_entry["album"] = {
                "name": album["#text"],
                "mbid": album["mbid"],
                "artist_id": artist["mbid"]
            }
            clean_history.append(clean_entry)
    except TypeError as te:
        print("Could not clean data due to:")
        print(te, "\nRaw data might not be on lastfm format.")
    return clean_history


def save_clean_data(source_file=LASTFM_FILENAME, source_format="lastfm",
                    destination_file=CLEANED_FILENAME):
    """Saves a cleaned version of the music history.

    Currently implemented for LastFM data
    """
    data = load_json_history(source_file)
    cleaned_data = {"not_working": "not working"}
    if source_format == "lastfm":
        cleaned_data = clean_lfm_data(data)

    save_json_history(destination_file, cleaned_data)


def fill_database(history_filename=CLEANED_FILENAME, db_filename=DB_FILENAME):
    """Fills given database with given cleaned data

    history_filename: path to json file with clean data
    db_filename: path to the database that shall be filled
    """
    json_history = load_json_history(history_filename)
    db.create_connection(db_filename)
    db.fill_tables(json_history, db_filename)
