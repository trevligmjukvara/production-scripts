# Trevlig Mjukvara Production Scripts
Scripts used to produce episodes of Trevlig Mjukvara.

## Requirements

- ffmpeg
- ffmpeg-normalize
- sox
- chapters-support:
    - mp3chaps (pip3 install mp3chaps)
    - tinytag (pip3 install tinytag)
    - pydub (pip install pydub)
- audio-visualizer-python (see https://github.com/trevligmjukvara/audio-visualizer-python )

## Assumptions

### Folder structure

The scripts assume that they are placed in a certain folder structure... 
- Finished Episodes
- Recordings
    - produce-chapters.py <--  
    - produce-episode.sh <-- 
    - EpisodeRecordings1
    - EpisodeRecordings2
    - ...


## Usage
1. stand in the "Recordings" folder
1. `./produce-episode.sh MIXED_RECORDINGS_FOLDER`

