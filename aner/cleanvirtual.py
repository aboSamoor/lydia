#! /usr/bin/env python

import os
import sys
import lydia.aner.tools as tools

if __name__ == "__main__":
    fName = os.path.abspath(sys.argv[1])
    lines = tools.loadJson(fName)
    newLines = []
    for i in range(len(lines)):
        if lines[i]["virtual"] == False:
            newLines.append(lines[i])
    tools.dumpJson(newLines,fName)
