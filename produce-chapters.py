#!/usr/bin/env python
# *-* encoding: utf-8 -*-
"""
Usage:
  produce-chapters.py <part1_flac> <audacity_labels_part1> <audacity_labels_part2_file> <target_mp3>
"""

from eyed3.id3 import Tag
from eyed3 import core
import os
import sys
from docopt import docopt
from tinytag import TinyTag  # for flac length parsing
from pydub import AudioSegment
from pathlib import Path
import subprocess
import tempfile


class Chapter:
    start = 0
    end = 0
    title = "title"


def parse_chapters_file(fname, offset_ms):
    chaps = []
    with open(fname, "r") as f:
        for line in f.readlines():
            time, title = line.split()[0], u" ".join(line.split()[2:])
            timeMs = int((float(time)*1000) + offset_ms)
            chap = Chapter()
            chap.start = timeMs
            chap.title = title
            chaps.append(chap)
            print("{} seconds in: '{}'".format(timeMs/1000, title))
    return chaps


def add_chapters(fname, chaps):
    tag = Tag()
    tag.parse(fname)
    audioFile = core.load(fname)
    total_length = audioFile.info.time_secs * 1000
    tag.setTextFrame(b"TLEN", str(int(total_length)))
    for i, chap in enumerate(chaps):
        if i < (len(chaps)-1):
            chap.end = chaps[i+1].start

    chaps[-1].end = total_length

    index = 0
    child_ids = []
    for chap in chaps:
        element_id = "ch{}".format(index).encode()
        print("Adding chapter {} at {}".format(chap.title, chap.start))
        new_chap = tag.chapters.set(element_id, (chap.start, chap.end))
        new_chap.sub_frames.setTextFrame(b"TIT2", u"{}".format(chap.title))
        child_ids.append(element_id)
        index += 1
    tag.table_of_contents.set(b"toc", child_ids=child_ids)
    list_chaps(tag)
    tag.save()


def generate_video_per_chapter(fname, chaps, chapters_folder, title, bg_img_neutral, bg_img_evil, bg_img_good, bg_img_bloopers):
    with tempfile.TemporaryDirectory() as tmpdir:
        audio = AudioSegment.from_mp3(fname)
        ignored_chapters = ["outro", "intro", "utmaningar", "meta"]
        wanted_chapters = list(
            filter(lambda x: x.title.lower() not in ignored_chapters, chaps))
        done_chapters = 0
        Path(chapters_folder).mkdir(parents=True, exist_ok=True)
        for chap in wanted_chapters:
            chapter_audio = audio[chap.start:chap.end].fade_in(
                1000).fade_out(1000)
            chapter_audio_file = tmpdir + "/" + chap.title + ".mp3"
            chapter_video_file = tmpdir + "/" + chap.title + ".mp4"
            output_chapter_video_file = chapters_folder + chap.title + ".mp4"
            chapter_video_title = title.upper() + " • " + chap.title
            # export mp3
            chapter_audio.export(chapter_audio_file, format="mp3")

            background_image_file = bg_img_neutral
            if chap.title.lstrip().lower().startswith("blooper"):
                background_image_file = bg_img_bloopers
            elif chap.title.lstrip().lower().startswith("otrevlig"):
                background_image_file = bg_img_evil
            elif chap.title.lstrip().lower().startswith("trevlig"):
                background_image_file = bg_img_good

            # produce video
            subprocess.run(["audio-visualizer-python", "-i", chapter_audio_file, "-o", chapter_video_file, "-t", chapter_video_title,
                            "-b", background_image_file, "-C", "250,250,250", "-a", "1", "-x", "640", "-f", "Sulphur Point"])
            # merge audio with video
            subprocess.run(["ffmpeg", "-i", chapter_video_file, "-i", chapter_audio_file,
                            "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", output_chapter_video_file])

            done_chapters += 1
            if done_chapters < len(wanted_chapters):
                print("{} of {} chapters done.".format(
                    done_chapters, len(wanted_chapters)))
            else:
                print("All chapters exported!")


def list_chaps(tag):
    "list chapters in tag"
    print("Chapters:")
    for chap in tag.chapters:
        print(chap.sub_frames.get(b"TIT2")[0]._text)


def main():
    "Entry point"
    print("Part1 {}, target {}".format(sys.argv[1], sys.argv[2]))
    part1_length = TinyTag.get(sys.argv[1]).duration * 1000
    print("P1 length: {} s".format(part1_length / 1000))
    chapters_p1_file = sys.argv[2]
    chapters_p2_file = sys.argv[3]
    target_mp3 = sys.argv[4]
    chapters_folder = sys.argv[5]
    title = sys.argv[6]
    bg_image_file = sys.argv[7]
    bg_image_file_evil = sys.argv[8]
    bg_image_file_good = sys.argv[9]
    bg_image_file_bloopers = sys.argv[10]

    chapters = []
    chapters += parse_chapters_file(chapters_p1_file, 0)
    chapters += parse_chapters_file(chapters_p2_file, part1_length)
    print(len(chapters))

    add_chapters(target_mp3, chapters)
    print("MP3 PRODUCED -- generating chapter videos")
    generate_video_per_chapter(
        target_mp3, chapters, chapters_folder, title, bg_image_file, bg_image_file_evil, bg_image_file_good, bg_image_file_bloopers)


if __name__ == '__main__':
    main()
