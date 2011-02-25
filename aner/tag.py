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

def print_exception():
    exc_type, exc_value = sys.exc_info()[:2]
    print 'Handling %s exception with message "%s"' % \
        (exc_type.__name__, exc_value)

def tagFile(f, dictionary):
    try:
        jText = json.load(open(f, 'r'))
    except:
        print "Error "+ f +" failed to be loaded"
        print_exception()
        return -1
    jNewText = tag(jText, dictionary)
    fh = open(f+".t", 'w')
    try:
        json.dump(jNewText, fh)
        fh.close()
    except:
        print "Error "+ f +" failed to be written"
        print_exception()
        fh.close()
        os.remove(f+".t")

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

