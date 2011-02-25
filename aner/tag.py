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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: tag.py dictionary file\nfile expected in json format"
    f = os.path.abspath(sys.argv[2])
    dicName = os.path.abspath(sys.argv[1])
    dictionary = pickle.load(open(dicName,'r'))
    if not os.path.isfile(f):
        print "usage: tag.py dictionary fileName ....." 
        sys.exit()
    jText = json.load(open(f, 'r'))
    print f
    jNewText = tag(jText, dictionary)
    fh = open(f+".t", 'w')
    json.dump(jNewText, fh)
    fh.close()
