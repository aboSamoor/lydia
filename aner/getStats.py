#! /usr/bin/env python

import os
import sys
import settings
import re
import tools
import pickle



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
    folder = os.path.abspath(sys.argv[1])
    for fName in tools.files(folder, "(.*?)\.t$"):
        fName = os.path.abspath(fName)
        print fName
        partial = parsePostNER(fName)
        add2Results(partial, results)
    statFile = os.path.join(folder, 'stats')
    fh = open(statFile,'w')
    print results
    pickle.dump(results,fh)
    fh.close()
