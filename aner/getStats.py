#! /usr/bin/env python

import os
import sys
import settings
import re
import tools


def isNNP(line):
    return line["POS"][:3] == "NNP"

def isNNPVirt(line):
    try:
        if len(line["POS"]) > 2:
            return line["POS"][:3] == "NNP" and line["virtual"]
    except:
        print line
        return False

def parsePostNER(fin):
    statistics = {}
    text = tools.getText(fin)
    for line in text.splitlines():
        if line != '':
            cols = [word for word in line.split('\t')]
            if len(cols) != 5:
                print line
                print "not well formatted line"
                continue
            else:
                if cols[1] == 'NNP':
                    if not statistics.has_key(cols[0]):
                        statistics[cols[0]] = {}
                    if not statistics[cols[0]].has_key(cols[4]):
                            statistics[cols[0]][cols[4]]=0
                    statistics[cols[0]][cols[4]] += 1
    return statistics

def parseJson(fin, constraint, feature):
    jText = tools.loadJson(fin)
    if jText == -1:
        return -1
    statistics = {}
    lines = filter(constraint, jText)
    for line in lines:
        if not statistics.has_key(line["word"]):
            statistics[line["word"]] = {}
        if not statistics[line["word"]].has_key(line[feature]):
            statistics[line["word"]][line[feature]] = 0
        statistics[line["word"]][line[feature]] += 1 
    return statistics

def add2Results(partial, store):
    for k in partial.keys():
        for v in partial[k].keys():
            if not store.has_key(k):
                store[k] = {}
            if not store[k].has_key(v):
                store[k][v] = 0
            store[k][v] += partial[k][v]
    return store

if __name__=="__main__":
    amira_dir = settings.amira_dir
    results = {}
    if len(sys.argv) < 3:
        print "usage: getStats.py folder format[json|...]\nFolder should contain files in .t extension"
    folder = os.path.abspath(sys.argv[1])
    fmt  = sys.argv[2]
    i = 0
    for fName in tools.files(folder, ".*"):
        fName = os.path.abspath(fName)
        if fmt == 'json':
            if i%100 == 0:
                print  i, " files finished"
            partial = parseJson(fName, isNNPVirt, "NER")
            i+=1
        else:
            partial = parsePostNER(fName)
        add2Results(partial, results)
    statFile = os.path.join(folder, 'stats')
    tools.dumpJson(results, statFile)
