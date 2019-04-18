#! /usr/bin/python3
import sys
from collections import defaultdict
import os
import json
import time

class MapInfrequent(object):

    def __init__(self, train_in, train_out):
        self.map = defaultdict(int)
        self.train_input = train_in
        self.train_output = train_out

    def format_tree(self,tree):
        if len(tree) == 2:
            if tree[1] != '.':
                if self.map.get(tree[1]) < 5:
                    tree[1] = "_RARE_"
        elif len(tree) == 3:
            self.format_tree(tree[1])
            self.format_tree(tree[2])

    def read(self):
        with open("cfg.counts", "r") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    if parts[1] == 'UNARYRULE':
                        lenOfData = len(parts)
                        num = int(parts[0])
                        word = parts[lenOfData-1]
                        self.map[word] = self.map.get(word, 0) + num

    def write(self):
        with open(self.train_input, "r") as fp:
            with open(self.train_output, "w+") as fw:
                for line in fp:
                    if line.strip():
                        parts = json.loads(line)
                        self.format_tree(parts)
                        newline = json.dumps(parts)
                        fw.write(newline + "\n")
                    elif not line.strip():
                        fw.write(line)


#-------------------q5-q6---------------------------#
class TrainKey(object):
    def __init__(self, train_rare_input, sentence_input, output_predict):
        self.map = defaultdict(int)
        self.train_rare = train_rare_input
        self.input_sentence = sentence_input
        self.out_predict = output_predict
        self.nonterminal = {}   #count(X)
        self.rule = {}
        self.unaryMatch = {}
        self.binaryMatch = {}
        self.rule_pro = defaultdict(lambda: float(0))     #q(x->yz)

    def get_rule_count(self):
        with open("cfg_RARE.counts") as fp:
            for line in fp:
                if line.strip():
                    parts = line.strip().split(" ")
                    if parts[1] == 'NONTERMINAL':
                        self.nonterminal[parts[2]] = self.nonterminal.get(parts[2], 0) + int(parts[0])
                    elif parts[1] == 'UNARYRULE':
                        self.rule[parts[2],parts[3]] = int(parts[0])
                        if parts[3] in self.unaryMatch:
                            self.unaryMatch[parts[3]].append(parts[2])
                        else:
                            self.unaryMatch[parts[3]] = [parts[2]]
                    elif parts[1] == 'BINARYRULE':
                        self.rule[parts[2],parts[3],parts[4]] = int(parts[0])
                        if parts[2] in self.binaryMatch:
                            self.binaryMatch[parts[2]].append([parts[3], parts[4]])
                        else:
                            self.binaryMatch[parts[2]] = [[parts[3], parts[4]]]

    def get_rule_prob(self):
        #calculate all rule Prob
        for key, val in self.rule.items():
            countX = self.nonterminal.get(key[0])
            prob = float(val)/countX
            self.rule_pro[key] = prob



    def ckyAlgo(self, words):
        pi = defaultdict(lambda: 0)
        bp = defaultdict(tuple)
        leng = len(words)
        for i in range (1,leng+1):
            word = words[i-1]
            if word in self.unaryMatch:
                for tag in self.unaryMatch[word]:
                    pi[i, i, tag] = self.rule_pro[tag, word]
                    bp[i, i, tag] = [word]
            else:
                for tag_rare in self.unaryMatch["_RARE_"]:
                    pi[i,i, tag_rare] = self.rule_pro[tag_rare, "_RARE_"]
                    bp[i,i, tag_rare] = [word]


        for l in range(1, leng):
            for i in range(1, leng-l+1):
                j = i + l
                for key in self.binaryMatch:
                    max_p = 0
                    max_b = {}
                    for val in self.binaryMatch.get(key):
                        if (key, val[0], val[1]) in self.rule_pro:
                            for s in range(i,j):
                                pi_t = self.rule_pro[key, val[0], val[1]]*pi[i,s,val[0]]*pi[s+1,j,val[1]]
                                if pi_t > max_p:
                                    max_p = pi_t
                                    max_b = (val[0], s, val[1])
                            pi[i, j, key] = max_p
                            bp[i, j, key] = max_b


        if pi[1,leng,'S'] == 0:
            max_p = 0
            Start = ""
            for X in self.nonterminal:
                if pi[1,leng,X] > max_p:
                    max_p = pi[1, leng, X]
                    Start = X
            return self.format_tree(1, leng, bp, Start)
        else:
            return self.format_tree(1, leng, bp, 'S')



    def format_tree(self,i,j,bp,start):
        if len(bp[i, j, start]) == 3:
            Y = bp[i, j, start][0]
            S = bp[i, j, start][1]
            Z = bp[i, j, start][2]
            return [start, self.format_tree(i, S, bp, Y), self.format_tree(S+1, j, bp, Z)]
        else:
            return [start, bp[i, j, start][0]]


    def getTagSeq(self):
        with open(self.input_sentence, "r") as fp:
            with open(self.out_predict, "w+") as fw:
                for line in fp:
                    if line.strip():
                        words = line.strip().split(" ")
                        tree = self.ckyAlgo(words)
                        newline = json.dumps(tree) + '\n'
                        fw.write(newline)




if __name__ == "__main__":
    if sys.argv[1] == "q4":
        train_input = sys.argv[2]
        train_output = sys.argv[3]
        os.system('python3 count_cfg_freq.py ' + train_input + ' > cfg.counts')
        map1 = MapInfrequent(train_input, train_output)
        map1.read()
        map1.write()
    elif sys.argv[1] == 'q5':
        train_rare_input = sys.argv[2]
        sentence_input = sys.argv[3]
        output_predict = sys.argv[4]
        os.system('python3 count_cfg_freq.py ' + train_rare_input + ' > cfg_RARE.counts')
        map2 = TrainKey(train_rare_input, sentence_input, output_predict)
        map2.get_rule_count()
        map2.get_rule_prob()
        map2.getTagSeq()
    elif sys.argv[1] == 'q6':
        train_rare_input = sys.argv[2]
        sentence_input = sys.argv[3]
        output_predict = sys.argv[4]
        os.system('python3 count_cfg_freq.py ' + train_rare_input + ' > cfg_RARE.counts')
        map2 = TrainKey(train_rare_input,sentence_input,output_predict)
        map2.get_rule_count()
        map2.get_rule_prob()
        map2.getTagSeq()
