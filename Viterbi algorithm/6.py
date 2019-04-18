#! /usr/bin/python3
from collections import defaultdict
import math
import os
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
            with open("ner_train_new.dat", "a+") as fw:
                for line in fp:
                    if line.strip():
                        parts = line.strip().split(" ")
                        word = parts[0]
                        tag = parts[1]
                        if self.map.get(word) < 5:
                            if word.isdigit():
                                word = "_DATE_"
                            elif any(x.isupper() for x in word):
                                word = "_CAP_"
                            elif any(x.isdigit() for x in word) and any(x == "," for x in word):
                                word = "_NUM_"
                            else:
                                word = "_RARE_"
                        line = word + " " + tag
                        fw.write(line + "\n")
                    elif not line.strip():
                        fw.write(line)


class ViterbiAlgo(object):
    def __init__(self):
        self.wordMap = {}
        self.tagMao = {}
        self.pi = {}
        self.set = set()
        self.word = {}
    def readTagCount(self):
        with open("ner_new.counts","r") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    count = float(parts[0])
                    if parts[1].endswith("GRAM"):
                        n = int(parts[1].replace("-GRAM", ""))
                        if n == 2:
                            self.tagMao[(parts[2], parts[3])] = count
                        elif n == 3:
                            self.tagMao[(parts[2], parts[3], parts[4])] = count
                        elif n == 1:
                            self.tagMao[(parts[2])] = count
                            self.set.add(parts[2])
                    elif parts[1] == "WORDTAG":
                        ne_tag = parts[2]
                        word = parts[3]
                        if word not in self.word:
                            list = []
                            list.append(ne_tag)
                            self.word[word] = list
                        else:
                            self.word[word].append(ne_tag)
                        self.wordMap[(word,ne_tag)] = count


    def pi_viterbi(self,k, u, v, wordPrePre,e,piPre):
        prob = defaultdict(float)
        # initialization
        for w in wordPrePre:
            # tuple((w,u,v))
            if (w, u, v) not in self.tagMao:
                self.tagMao[w, u, v] = 0
            if (w, u) not in self.tagMao:
                self.tagMao[w, u] = 0
            if v not in self.tagMao:
                self.tagMao[v] = 0

            if self.tagMao[w,u] == 0 or self.tagMao[w,u,v] == 0:
                q = -math.inf
            else:
                q = math.log2(self.tagMao[w, u, v]) - math.log2(self.tagMao[w,u])
            if tuple((k-1,w,u)) not in piPre:
                prev = -math.inf
            else:
                prev = piPre[tuple((k-1,w,u))]

            probability = prev + q + e
            prob[tuple((w, u))] = probability
        max_tuple = max(prob.items(), key=lambda x: x[1])
        return max_tuple[1], max_tuple[0][0]

    def getWordList(self, k):
        if k < 0:
            return set(["*"])
        else:
            return self.set

    def getWordTaglist(self,word):
        if word in self.word:
            return word, self.word[word]
        else:
            if word.isdigit():
                word = "_DATE_"
            elif any(x.isupper() for x in word):
                word = "_CAP_"
            elif any(x.isdigit() for x in word) and any(x == "," for x in word):
                word = "_NUM_"
            else:
                word = "_RARE_"
            return word, self.word[word]

    def algo(self,list):
        backpointer = defaultdict(str)
        tags = defaultdict(str)
        piPre = defaultdict(float)
        piPre[(0,"*","*")] = 0
        n = len(list)
        for i in range(1, n+1):
            prob = defaultdict(float)
            word,wordList = self.getWordTaglist(list[i-1])
            wordPre = self.getWordList(i-2)
            wordPrePre = self.getWordList(i-3)

            for v in wordList:
                for u in wordPre:
                    e = -math.inf
                    vCount = self.wordMap[word, v]
                    e = math.log2(vCount) - math.log2(self.tagMao[v])
                    value, w = self.pi_viterbi(i, u, v, wordPrePre, e, piPre)
                    prob[tuple((i, u, v))] = value
                    piPre[tuple((i, u, v))] = value
                    backpointer[tuple((i, u, v))] = w
            max_tuple = max(prob.items(), key=lambda x: x[1])

            self.pi[i] = max_tuple[1]
            u_glob = max_tuple[0][1]
            v_glob = max_tuple[0][2]

        tags[n - 1] = u_glob
        tags[n] = v_glob

        for i in range((n - 2), 0, -1):
            tag = backpointer[tuple(((i + 2), tags[i + 1], tags[i + 2]))]
            tags[i] = tag

        return tags

    def getTagSeq(self):
        with open("ner_dev.dat","r") as fp:
            with open("6.txt", "a+") as fw:
                list = []
                for line in fp:
                    if line.strip():
                        list.append(line.strip())
                    else:
                        if len(list) > 0:
                            tags = self.algo(list)
                            n = len(list)
                            for i in range(0,n):
                                newline = list[i] + " " + tags[i+1] + " " + repr(self.pi[i+1])
                                fw.write(newline+"\n")
                            self.pi.clear()
                            list.clear()
                        fw.write(line)

if __name__ == "__main__":
    map = MapInfrequent()
    map.read()
    map.write()
    os.system('python2 count_freqs.py ner_train_new.dat > ner_new.counts')
    map2 = ViterbiAlgo()
    map2.readTagCount()
    map2.getTagSeq()


