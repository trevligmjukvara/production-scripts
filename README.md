# Trevlig Mjukvara Production Scripts
Scripts used to produce episodes of Trevlig Mjukvara.

## Requirements

- ffmpeg
- ffmpeg-normalize
- sox
- avp (audio-visualizer-python, feature-newgui branch) 

## Assumptions

### Folder structure

The scripts assume that they are placed in a certain folder structure... 
- Finished Episodes
- Recordings
    - produce-video.sh <--  
    - produce-episode.sh <-- 
    - EpisodeRecordings1
    - EpisodeRecordings2
    - ...

### Others
- avp needs to have a "tm_template" template saved beforehand with two texts in the top two layers. 
- And many more forgotten ones.

## Usage

`./produce-episode.sh MIXED_RECORDINGS_FOLDER TITLE SUBTITLE`

