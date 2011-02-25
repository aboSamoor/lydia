#! /usr/bin/env python

import os
import sys
import tools
import pickle
import json

def localGroup(fName):
    jText = json.load(open(fName,'r'))
    f = open(fName+'.o','w')
    lines = jText
    length = len(lines)
    i = 0
    result = []
    while i < length:
        curLine = lines[i]
        newLine = curLine
        txt2 = ''
        if curLine["NER"]== "PER":
            while curLine["NER"] == "PER" or curLine["POS"] =="DET":
                txt2 = txt2 + curLine["word"] +' ' 
                i = i+1
                curLine = lines[i]
            i = i-1
            newLine["word"] = txt2
        elif curLine["NER"]== "LOC":
            while curLine["NER"] == "LOC"  or curLine["POS"] =="DET":
                txt2 = txt2 +curLine["word"]+' '
                i = i+1
                curLine = lines[i]
            i = i-1
            newLine["word"] = txt2
        elif curLine["NER"]== "ORG":
            while curLine["NER"] == "ORG" or curLine["POS"] =="DET":
                txt2 = txt2+curLine[0]+' '
                i = i+1
                curLine = lines[i]
            i = i-1
            newLine["word"] = txt2
        else:
            newLine["word"] = curLine["word"]            
        i = i+1
        result.append(newLine)
    json.dump(result,f)
    f.close()
    
    

if __name__ == "__main__":
    fName = os.path.abspath(sys.argv[1])    
    localGroup(fName)
