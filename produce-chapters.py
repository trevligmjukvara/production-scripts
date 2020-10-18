#!/usr/bin/env python
# *-* encoding: utf-8 -*-
"""
Usage:
  produce-chapters.py <part1_mp3?> <audacity_labels_part1> <audacity_labels_part2_file> <target_mp3>
"""

from eyed3.id3 import Tag
from eyed3 import core
import os
import sys
from docopt import docopt
from tinytag import TinyTag  # for flac length parsing


def parse_chapters_file(fname, offset_ms):
    filename = os.path.splitext(fname)
    chaps = []
    with open(fname, "r") as f:
        for line in f.readlines():
            time, title = line.split(2)[0], " ".join(line.split()[1:])
            print("Wazup " + title)
            chaps.append((int((float(time)*1000) + offset_ms), title))
    return chaps


def add_chapters(tag, fname, chaps):
    audioFile = core.load(fname)
    total_length = audioFile.info.time_secs * 1000
    tag.setTextFrame(b"TLEN", str(int(total_length)))
    chaps_ = []
    for i, chap in enumerate(chaps):
        if i < (len(chaps)-1):
            chaps_.append(((chap[0], chaps[i+1][0]), chap[1]))
    chaps_.append(((chaps[-1][0], total_length), chaps[-1][1]))
    index = 0
    child_ids = []
    for chap in chaps_:
        element_id = "ch{}".format(index).encode()
        times, title = chap
        new_chap = tag.chapters.set(element_id, times)
        new_chap.sub_frames.setTextFrame(b"TIT2", u"{}".format(title))
        child_ids.append(element_id)
        index += 1
    tag.table_of_contents.set(b"toc", child_ids=child_ids)
    tag.save()


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
    chapters.append(parse_chapters_file(chapters_p1_file, 0))
    chapters.append(parse_chapters_file(chapters_p2_file, part1_length))

    add_chapters(tag, target_mp3, chapters)


if __name__ == '__main__':
    main()
