#! /usr/bin/env python

import os
import sys
import tools
import pickle

def tag(fName, dic):
    tagged = []
    txt = tools.getText(fName)
    lines = txt.splitlines()
    for i in range(len(lines)):
        if lines[i] != '':
            words = lines[i].split('\t')
            newline = words
            newline[-1] = 'O'
            if words[1][:3] == "NNP":
                if not dic.has_key(words[0]):
                    if i > 0:
                        prevLine = tagged[-1]
                        if len(prevLine) > 1:
                            if len(prevLine[1]) > 2:
                                if prevLine[1][:3] == "NNP":
                                    newline[-1] = prevLine[-1]
                                elif prevLine[1] == "DET":
                                    if i > 1:
                                        prev2Line = tagged[-2]
                                        if len(prev2Line) > 1:
                                            if len(prev2Line[1]) > 2:
                                                if prev2Line[1][:3] == "NNP":
                                                    newline[-1] = prev2Line[4]
                else:
                    newline[-1] = list(dic[words[0]])[0]
            tagged.append(newline)
        else:
            tagged.append([''])
    newTxt = '\n'.join(['\t'.join(l) for l in tagged])
    tools.writeText(fName+".t",newTxt)

if __name__ == "__main__":
    folder1 = os.path.abspath(sys.argv[1])
    dicName = os.path.abspath(sys.argv[2])
    dictionary = pickle.load(open(dicName,'r'))
    if not os.path.isdir(folder1) or not os.path.isfile(dicName):
        print "usage: ....." 
        sys.exit()
    for fName in tools.files(folder1, "(.*?)\.NER$"):
        tag(fName, dictionary)
