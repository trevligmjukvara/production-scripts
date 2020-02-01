#!/bin/bash

start_time=`date +%s`

LOGCOLOR='\033[0;36m'
NC='\033[0m'

LOG () {
    echo "$(tput setaf 6)$1$(tput sgr0)"
}

LOG "REMOVING OLD STUFF"
mkdir .video_artifacts
rm -rf .video_artifacts/* 

LOG "RUNNING AVP"
avp tm_template --comp 98 text "title=$3" --comp 99 text "title=$2" -i "../Finished Episodes/$1.mp3" -o ".video_artifacts/$1.mkv"
ffmpeg -i ".artifacts/$1.mkv" -i "../Finished Episodes/$1.mp3" -c copy -map 0:v:0 -map 1:a:0 "../Finished Episodes/$1.mkv"

end_time=`date +%s`


LOG "VIDEO PRODUCED IN $((end_time-start_time)) SECONDS" 
