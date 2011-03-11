#! /usr/bin/env python

import os
import sys
import tools
import pickle
import json

def isNNP(line):
    if line["word"] != '':
        if line["POS"][:3] == "NNP":
            return True
    return False

def tag(jText, dic):
    tagged = []
    lines = jText
    for i in range(len(lines)):
        curLine = lines[i]
        curLine["NER"] = 'O'
        if isNNP(curLine):
            if not dic.has_key(curLine["word"]):
                if i > 0:
                    if isNNP(lines[i-1]):
                        curLine["NER"] = lines[i-1]["NER"]
                    elif lines[i-1]["POS"] == "DET":
                        if i > 1:
                            if isNNP(lines[i-2]):
                                curLine["NER"] = lines[i-2]["NER"]
            else:
                curLine["NER"] = list(dic[curLine["word"]])[0]
    return jText


def tagFile(f, dictionary):
    jText = tools.loadJson(f)
    if jText == -1:
        return -1
    jNewText = tag(jText, dictionary)
    tools.dumpJson(jNewText, f+".t")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: tag.py dictionary file\nfile expected in json format"
    f = os.path.abspath(sys.argv[2])
    dicName = os.path.abspath(sys.argv[1])
    dictionary = pickle.load(open(dicName,'r'))
    if os.path.isfile(f):
        tagFile(f, dictionary)
    elif os.path.isdir(f):
        i = 0
        for fName in tools.files(f, ".*\.json$"):
            if i%100 == 0:
                print "finished", i, "files"
            tagFile(fName,dictionary)
            i+=1

