#! /usr/bin/env python

import os
import sys
import tools
import pickle

def localGroup(fName):
    txt = tools.getText(fName)
    lines = txt.splitlines()
    length = len(lines)
    i = 0
    txt2 = ''
    while i < length:
        words = lines[i].split(' ')
        print words    
        print words[-1]
        if words[-1]== "PER":
            while words[-1] == "PER":
                txt2 = txt2 +' '+ words[0]
                i = i+1
                words = lines[i].split(' ')
            txt2 = txt2+' PER\n'
            i = i-1
        elif words[-1]== "LOC":
            while words[-1] == "LOC":
                txt2 = txt2 +' '+ words[0]
                i = i+1
                words = lines[i].split(' ')
            txt2 = txt2+' LOC\n'
            i = i-1
        elif words[-1]== "ORG":
            while words[-1] == "ORG":
                txt2 = txt2 +' '+ words[0]
                i = i+1
                words = lines[i].split(' ')
            txt2 = txt2+' ORG\n'
            i = i-1
        else:
            txt2 = txt2+words[0]+' '+words[-1]+'\n'
            print txt2
        i = i+1
    tools.writeText(fName+'.o',txt2)    

if __name__ == "__main__":
    fName = os.path.abspath(sys.argv[1])    
    localGroup(fName)
