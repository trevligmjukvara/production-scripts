#!/bin/bash

cd $1

start_time=`date +%s`

LOGCOLOR='\033[0;36m'
NC='\033[0m'

LOG () {
    echo "$(tput setaf 6)$1$(tput sgr0)"
}


LOG "REMOVING OLD STUFF"
mkdir .artifacts
rm -rf .artifacts/* 


LOG "(1/7) STITCHING"
ffmpeg -i alex-1.flac -i alex-2.flac \
-filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' \
-map '[out]' .artifacts/alex-stitched.flac &

ffmpeg -i seb-1.flac -i seb-2.flac \
-filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' \
-map '[out]' .artifacts/seb-stitched.flac &

ffmpeg -i sb-1.flac -i sb-2.flac \
-filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' \
-map '[out]' .artifacts/sb-stitched.flac &

wait

LOG "(2/7) HIGH-LOW VOICE PASS"
ffmpeg -y -i .artifacts/alex-stitched.flac -af highpass=110,lowpass=7700 .artifacts/alex-passes.flac &
ffmpeg -y -i .artifacts/seb-stitched.flac -af highpass=125,lowpass=7000 .artifacts/seb-passes.flac &
wait


LOG "(3/7) NORMALIZE VOICES"
ffmpeg-normalize .artifacts/alex-passes.flac .artifacts/seb-passes.flac -tp 0 -of .artifacts -ext flac -c:a flac --dual-mono -f --progress


LOG "(4/7) PRE NORMALIZER COMPRESSOR/LIMITER/GAINER"
ffmpeg -y -i .artifacts/alex-passes.flac -filter_complex "compand=points=-40/-900|-35/-30|-30/-20|-25/-18|-20/-13|-15/-10|-10/-5|0/0|20/0" -ar 44100 .artifacts/alex-compressed.flac &
ffmpeg -y -i .artifacts/seb-passes.flac -filter_complex  "compand=points=-40/-900|-35/-30|-30/-20|-25/-16|-20/-13|-15/-10|-10/-5|0/0|20/0" -ar 44100 .artifacts/seb-compressed.flac &
wait

LOG "(5/7) NORMALIZE SOUNDBOARD"
ffmpeg-normalize .artifacts/sb-stitched.flac -o .artifacts/sb.flac --normalization-type peak --target-level -4 -c:a flac -f --progress


LOG "(6/7) MERGE ALL"
sox -M .artifacts/sb.flac .artifacts/alex-compressed.flac .artifacts/seb-compressed.flac .artifacts/all.flac remix -m -p 1,3,4 2,3,4


LOG "(7/7) PRODUCE MP3"
ffmpeg -y -i .artifacts/all.flac -vn -ar 44100 -ac 2 -ab 192k -f mp3 -joint_stereo 1 "../../Finished Episodes/$1-192.mp3"

audio_prod_time=`date +%s`
LOG "AUDIO PRODUCED IN $((audio_prod_time-start_time)) SECONDS"

LOG "(BONUS) ADD CHAPTERS TO MP3, produce video"
../produce-chapters.py alex-1.flac labels-1.txt labels-2.txt "../../Finished Episodes/$1-192.mp3" "../../Finished Episodes/clips/$1/" $1 "../../Branding/Banner/video-background-neutral.png" "../../Branding/Banner/video-background-evil.png" "../../Branding/Banner/video-background-good.png" "../../Branding/Banner/video-background-bloopers.png"

end_time=`date +%s`
LOG "EVERYTHING PRODUCED IN $((end_time-start_time)) SECONDS"
