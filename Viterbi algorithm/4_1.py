#! /usr/bin/python3
import sys
from collections import defaultdict
import math
def getCountTagAndWord(tag, name):
    with open(ner.counts) as fp:
        line = fp.readlines()
        cnt = 1
        while line:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1] == "WORDTAG":
                ne_tag = parts[2]
                word = parts[3]
                if (tag == ne_tag) and (name == word):
                    return count
    return -1

def getCountTag(tag):
    with open(ner.counts) as fp:
        line = fp.readlines()
        while line:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1].endswith("GRAM"):
                n = int(parts[1].replace("-GRAM", ""))
                ne_tag = parts[2]
                if n == 1 and ne_tag == tag:
                    return count
    return -1

def computeEmission(tag, name):
    count1 = getCountTagAndWord(tag,name)
    count2 = getCountTag(tag)
    res = 0.0
    if count1 != -1 and count2 != -1:
        res = float(count1/count2)

    return res


class MapInfrequent(object):

    def __init__(self):
        self.map = defaultdict(int)

    def read(self):
        with open("ner_train.dat", "r") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    word = parts[0]
                    self.map[word] = self.map.get(word, 0) + 1

    def write(self):
        with open("ner_train.dat", "r") as fp:
            with open("ner_train_rare.dat", "a+") as fw:
                for line in fp:
                    if line.strip():
                        parts = line.strip().split(" ")
                        word = parts[0]
                        tag = parts[1]
                        if self.map.get(word) < 5:
                            word = "_RARE_"
                        line = word + " " + tag
                        fw.write(line + "\n")
                    elif not line.strip():
                        fw.write(line)


if __name__ == "__main__":
    map = MapInfrequent()
    map.read()
    map.write()




