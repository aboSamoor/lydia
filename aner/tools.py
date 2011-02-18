#! /usr/bin/env python

import os
import sys
import NER
import re

def get_columns(text, delimiter, cols):
    result = []
    for line in text.splitlines():
        if line != '':
            templine = line.split(delimiter)
            newline = [templine[j] for j in cols]
            result.append(delimiter.join(newline))
        else:
            result.append(line)
    return '\n'.join(result)

def files(folder, pattern):
    folder = os.path.abspath(folder)
    ptrn = re.compile(pattern)
    if not os.path.isdir(folder):
        print "this is a file"
        yield ''
    for fName in os.listdir(folder):
        if ptrn.search(fName) and not os.path.isfile(fName+".bw.post.NER"):
            yield os.path.join(folder,fName)

def getBinary(fin):
    fin = os.path.abspath(fin)
    fh = open(fin, 'rb')
    binary = fh.read()
    fh.close()
    return binary

def writeUTF8(data, fout):
    fout = os.path.abspath(fout)
    fh = open(fout, 'w')
    text = data
    fh.write(text)
    fh.close()

def b2utf8(fin, fout):
    data = getBinary(fin)
    text = data.decode('utf-8','ignore')
    writeUTF8(data, fout)

def getText(fin):
    fin = os.path.abspath(fin)
    fh = open(fin, 'r')
    text = fh.read()
    fh.close()
    return text.decode('utf-8','ignore')

def writeText(fout, text):
    fout = os.path.abspath(fout)
    fh = open(fout, 'w')
    text = fh.write(text)
    fh.close()

def countCols(line, delim):
    return len(line.split(delim))
    
def fixCols(fin):
    txt = getText(fin)
    oneCol = re.compile(r"\n\w*\n")
    txt1 = oneCol.sub(". O",txt)
    endStmt = re.compile(r"(\n[!|?|.] O\n)")
    txt2 = endStmt.sub("\\1\n",txt1)
    writeText(fin+".fix",txt2)

def rows(text, delim):
    count = countCols(text.splitlines()[0], delim)
    for line in text.splitlines():
        if len(line.split(delim)) == count:
            yield line

if __name__== "__main__":
    fName = os.path.abspath(sys.argv[1])
    b2utf8(fName, fName+".utf8")
    NER.utf8tobw(fName+".utf8", fName+".BW")
    b2utf8(fName+".BW", fName+".BW.utf8")
    fixCols(fName+".BW.utf8")
    
    
