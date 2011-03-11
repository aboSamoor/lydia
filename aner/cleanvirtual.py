#! /usr/bin/env python

import os
import sys
import tools
import json

if __name__ == "__main__":
    fName = os.path.abspath(sys.argv[1])
    f = open(fName,'r')
    try:
        lines = json.load(f)
    except:
        sys.exit()
    newLines = []
    for i in range(len(lines)):
        if lines[i]["virtual"] == False:
            newLines.append(lines[i])
    fh = open(fName, 'w')
    try:
        json.dump(newLines,fh)
    except:
        print fName
            
        
