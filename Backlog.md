# Backlog for music history analysis:


## Sprint 1:
### - 02.04.2019
- [x] Refactor "song" to "track" --DONE
- [x] Add correct map-structure and setup/init for correct project configuration --DONE
- [x] Change db to have entry, track, album, artist table --DONE
- [x] Add functionality to output:
    - [x] total listens
    - [x] number of unique tracks
    - [x] number of unique albums
    - [x] number of unique artists
    - [x] most listened track
    - [x] most listened album
    - [x] most listened artist
- [x] Research pandas: is it right for this project, yes/no
    - yes.
    
## Sprint 2
### 02.04.2019 - 07.05.2019
- [x] Implement proper CLI tool
    - Now using Click python cli creation kit.
- [x] Refactor program to use Pandas
- [x] Decide on GUI 
    - PySimpleGUI:<br>
    Reasoning:<br>
    Actively developed and updated, supports many different options for gui, including web.
- [x] Implement more interesting statistics
    - [x] Time-bounded statistics
    - [x] Listens-per-hour
<s>
- [ ] Connect to spotify:</s><b> - Moved to next sprint</b><s>
    - get the spotify id for tracks, albums and artists in the lfm history
    - Retrieve for all entries in lfm history:
        - [ ] Spotify track_id
        - [ ] Spotify album_id
        - [ ] Spotify artist_id
        - [ ] Spotify category
</s> 

## Sprint 3
### 07.05.2019 - 
- [ ] Implement proper unit tests
- [ ] Set up Continuous integration
- [ ] Make statistics entries into objects
- [ ] Begin to implement GUI
    - [ ] Make simple window to house UI
- [ ] Create Spotify app for access to spotify api
    - [ ] Decide on name for project
    - [ ] Research app uris needed for the api
- [ ] Create readme.md for github page
- [ ] Implement more statistics
    - [ ] stats-per-hour
        - [ ] Tracks
        - [ ] Albums
        - [ ] Artists
    - [ ] Listens per month
    - [ ] Listens per day

