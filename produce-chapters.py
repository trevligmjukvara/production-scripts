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

class Chapter:
    start = 0
    end = 0
    title = "title"

def parse_chapters_file(fname, offset_ms):
    filename = os.path.splitext(fname)
    chaps = []
    with open(fname, "r") as f:
        for line in f.readlines():
            time, title = line.split()[0], u" ".join(line.split()[2:])
            timeMs = int((float(time)*1000) + offset_ms)
            chap = Chapter()
            chap.start = timeMs
            chap.title = title;
            chaps.append(chap)
            print("{} seconds in: '{}'".format( timeMs/1000, title))
    return chaps


def add_chapters(tag, fname, chaps):
    audioFile = core.load(fname)
    total_length = audioFile.info.time_secs * 1000
    tag.setTextFrame(b"TLEN", str(int(total_length)))
    for i, chap in enumerate(chaps):
        if i < (len(chaps)-1):
            chap.end = chaps[i+1].start

    chaps[-1].end = total_length;

    index = 0
    child_ids = []
    for chap in chaps:
        element_id = "ch{}".format(index).encode()
        print ("Adding chapter {} at {}".format(chap.title,chap.start))
        new_chap = tag.chapters.set(element_id, (chap.start, chap.end))
        new_chap.sub_frames.setTextFrame(b"TIT2", u"{}".format(chap.title))
        child_ids.append(element_id)
        index += 1
    tag.table_of_contents.set(b"toc", child_ids=child_ids)
    list_chaps(tag)
    tag.save()

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
    tag = Tag()
    tag.parse(target_mp3)

    chapters = []
    chapters += parse_chapters_file(chapters_p1_file, 0)
    chapters += parse_chapters_file(chapters_p2_file, part1_length)
    print (len(chapters))

    add_chapters(tag, target_mp3, chapters)


if __name__ == '__main__':
    main()
