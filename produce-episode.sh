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


LOG "(1/8) STITCHING"
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

LOG "(2/8) NORMALIZE VOICES"
ffmpeg-normalize .artifacts/alex-stitched.flac .artifacts/seb-stitched.flac -tp -1 -of .artifacts -ext flac -c:a flac --dual-mono -f --progress


LOG "(3/8) PRE NORMALIZER COMPRESSOR/LIMITER/GAINER"
ffmpeg -y -i .artifacts/alex-stitched.flac -filter_complex "compand=points=-40/-900|-35/-30|-30/-20|-25/-15|-20/-10|-10/-6|0/-3|20/-2" .artifacts/alex-compressed.flac &
ffmpeg -y -i .artifacts/seb-stitched.flac -filter_complex  "compand=points=-40/-900|-35/-30|-30/-20|-25/-15|-20/-10|-10/-6|0/-3|20/-2" .artifacts/seb-compressed.flac &
wait

LOG "(4/8) HIGH-LOW VOICE PASS"
ffmpeg -y -i .artifacts/alex-compressed.flac -af highpass=120,lowpass=7000 -ar 44100 .artifacts/alex-passes.flac &
ffmpeg -y -i .artifacts/seb-compressed.flac -af highpass=120,lowpass=7000 -ar 44100 .artifacts/seb-passes.flac &
wait

LOG "(5/8) NORMALIZE SOUNDBOARD"
ffmpeg-normalize .artifacts/sb-stitched.flac -o .artifacts/sb.flac --normalization-type peak --target-level -4 -c:a flac -f --progress


LOG "(6/8) MERGE ALL"
sox -M .artifacts/sb.flac .artifacts/alex-passes.flac .artifacts/seb-passes.flac .artifacts/all.flac remix -m -p 1,3,4 2,3,4


LOG "(7/8) DOWNWARD COMPRESSION"
ffmpeg -y -i .artifacts/all.flac  -af \
  acompressor=threshold=0.6:ratio=3:attack=15:release=100 \
  $1.flac

LOG "(8/8) PRODUCE MP3"
ffmpeg -y -i $1.flac -vn -ar 44100 -ac 2 -ab 320k -f mp3 -joint_stereo 1 "../../Finished Episodes/$1-320.mp3" &
ffmpeg -y -i $1.flac -vn -ar 44100 -ac 2 -ab 128k -f mp3 -joint_stereo 1 "../../Finished Episodes/$1-128.mp3" &
wait

end_time=`date +%s`


LOG "AUDIO PRODUCED IN $((end_time-start_time)) SECONDS"

sh ./produce-video.sh "$1-128" $2 $3
