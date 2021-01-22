#!/bin/bash

cd $1

start_time=`date +%s`

LOGCOLOR='\033[0;36m'
NC='\033[0m'

LOG () {
    echo "$(tput setaf 6)$1$(tput sgr0)"
}


LOG "ADD CHAPTERS TO MP3, RENDER VIDEO"
../produce-chapters.py alex-1.flac labels-1.txt labels-2.txt "../../Finished Episodes/$1-192.mp3" "../../Finished Episodes/clips/$1/" $1 "../../Branding/Banner/video-background-neutral.png" "../../Branding/Banner/video-background-evil.png" "../../Branding/Banner/video-background-good.png" "../../Branding/Banner/video-background-bloopers.png"

end_time=`date +%s`
LOG "EVERYTHING PRODUCED IN $((end_time-start_time)) SECONDS"
