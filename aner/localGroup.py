#! /usr/bin/env python

import os
import sys
import tools
import json

def group(lines, i, tag):
    parts = []
    curLine = lines[i]
    if not curLine["virtual"] and curLine["NER"] == tag:
        while curLine["NER"] == tag or curLine["POS"] =="DET":
            if not curLine["POS"] == "DET":
                parts.append(curLine["word"])
            else:
                parts.append("Al")
            i = i+1
            curLine = lines[i]
        if len(filter( lambda x: x != "Al", parts)) > 1:
            newLine = {"word": ' '.join(parts), "POS": "NNP", "NER": tag, "virtual": True, "POS1": '', "POS2":''}
            lines.append(newLine)
    return i

def localGroup(fName):
    lines = json.load(open(fName,'r'))
    i = 0
    while i < len(lines):
        j = i
        i = group(lines, i, "PER")
        i = group(lines, i, "LOC")
        i = group(lines, i, "ORG")
        if i == j:
            i += 1
    fh = open(fName, 'w')
    json.dump(lines, fh)
    fh.close()

if __name__ == "__main__":
    fName = os.path.abspath(sys.argv[1])    
    localGroup(fName)
