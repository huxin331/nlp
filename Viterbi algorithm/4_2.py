#! /usr/bin/python3
import math

def computeEmission(tag, name):
    count1 = getCountTagAndWord(tag,name)
    count2 = getCountTag(tag)
    res = 0.0
    if count1 != -1 and count2 != -1:
        res = float(count1/count2)

    return res


class Calulate(object):

    def __init__(self):
        self.wordmap = {}
        self.wordProb ={}
        self.tagCount = {}

    def readCount(self):
        with open("ner_rare.counts","r") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    count = float(parts[0])
                    if parts[1] == "WORDTAG":
                        ne_tag = parts[2]
                        word = parts[3]
                        newObj = [count, ne_tag]
                        if word not in self.wordmap:
                            list = []
                            list.append(newObj)
                            self.wordmap[word] = list
                        else:
                            self.wordmap[word].append(newObj)
                    elif parts[1].endswith("GRAM"):
                        n = int(parts[1].replace("-GRAM", ""))
                        ne_tag = parts[2]
                        if n == 1:
                            self.tagCount[ne_tag] = count


    def calculateProb(self):
        for key, value in self.wordmap.items():
            max = -float('inf')
            maxTag = ""
            for element in value:
                countNum = element[0]
                tag = element[1]
                countTag = self.tagCount[tag]
                prob = math.log2(countNum) - math.log2(countTag)
                if prob > max:
                    max = prob
                    maxTag = tag
            h = [max, maxTag]
            self.wordProb[key] = h


    def createNewFile(self):
        with open("ner_dev.dat", "r") as fp:
            with open("4_2.txt", "a+") as fw:
                for line in fp:
                    if line.strip():
                        word = line.strip()
                        if word in self.wordProb:
                            count = self.wordProb[word][0]
                            tag = self.wordProb[word][1]
                        else:
                            count = self.wordProb["_RARE_"][0]
                            tag = self.wordProb["_RARE_"][1]
                        newline = word + " " + tag + " " + repr(count)
                        fw.write(newline + "\n")
                    else:
                        fw.write(line)

if __name__ == "__main__":
    obj = Calulate()
    obj.readCount()
    obj.calculateProb()
    obj.createNewFile()

