#! /usr/bin/python3
import math
import sys
class CalulateTria(object):

    def __init__(self):
        self.map = {}

    def readCount(self):
        with open("ner_rare.counts","r") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    count = float(parts[0])
                    if parts[1].endswith("GRAM"):
                        n = int(parts[1].replace("-GRAM", ""))
                        if n == 2:
                            self.map[(parts[2],parts[3])] = count
                        elif n == 3:
                            self.map[(parts[2],parts[3],parts[4])] = count

    def creatNewFile(self):
        with open("trigrams.txt", "r") as fp:
            with open("5_1.txt", "a+") as fw:
                for line in fp:
                    if line.strip():
                        parts = line.strip().split(" ")
                        if (parts[0],parts[1],parts[2]) in self.map and (parts[0],parts[1]) in self.map:
                            ans = math.log2(self.map[parts[0],parts[1],parts[2]]) - math.log2(self.map[parts[0],parts[1]])
                            newline = line.strip() + " " + repr(ans)
                            fw.write(newline + "\n")
                        else:
                            ans = -math.inf
                            newline = line.strip() + " " + repr(ans)
                            fw.write(newline + "\n")
                    else:
                        fw.write(line)


if __name__ == "__main__":
    obj = CalulateTria()
    obj.readCount()
    obj.creatNewFile()

