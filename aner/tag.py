#! /usr/bin/env python

import os
import sys
import tools
import pickle
import json
import lydia.aner.csvConverter as csvConverter

def isTag(line, tag):
    if line["word"] != '':
        if len(line["POS"]) < len(tag):
            return False
        if line["POS"][:len(tag)] == tag:
            return True
    return False

def tag(jText, dic):
    tagged = []
    lines = jText
    for i in range(len(lines)):
        curLine = lines[i]
        curLine["NER"] = 'O'
        if isTag(curLine, "NNP"):
            if curLine["word"] in dic:
                curLine["NER"] = dic[curLine["word"]]["tag"]
            elif i > 0:
                    if isTag(lines[i-1],"NNP"):
                        curLine["NER"] = lines[i-1]["NER"]
                    elif isTag(lines[i-1],"DET"):
                        if i > 1:
                            if isTag(lines[i-2], "NNP"):
                                curLine["NER"] = lines[i-2]["NER"]
        #To detect Ahmad Al Khalidi
        #if Khalidi is not NNP
        elif isTag(curLine, "NN"):
            if i > 1:
                if isTag(lines[i-1],"DET"):
                    if isTag(lines[i-2], "NN"):
                        curLine["NER"] = lines[i-2]["NER"]
    return jText


def tagFile(f, dictionary):
    jText = tools.loadJson(f)
    if jText == -1:
        return -1
    jNewText = tag(jText, dictionary)
    tools.dumpJson(jNewText, f+".t")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: tag.py dictionary.csv file\nfile expected in json format"
    f = os.path.abspath(sys.argv[2])
    dicName = os.path.abspath(sys.argv[1])
    listOfDicts= csvConverter.csv2dicts(dicName)
    dictionary = csvConverter.buildDictionary(listOfDicts, "word")
    if os.path.isfile(f):
        tagFile(f, dictionary)
    elif os.path.isdir(f):
        i = 0
        for fName in tools.files(f, ".*\.json$"):
            if i%100 == 0:
                print "finished", i, "files"
            tagFile(fName,dictionary)
            i+=1
