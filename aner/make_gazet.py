#!/usr/bin/env python

import sys
import os
import settings
import re
import pickle


def getText(fin):
    fin = os.path.abspath(fin)
    fh = open(fin, 'r')
    text = fh.read()
    fh.close()
    return text

def writeText(fout, text):
    fout = os.path.abspath(fout)
    fh = open(fout, 'w')
    text = fh.write(text)
    fh.close()

def get_columns(text, delimiter, cols):
    result = []
    for line in text.splitlines():
        if line != '':
            templine = line.split(delimiter)    
            newline = [templine[j] for j in cols]
            print newline
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
        if ptrn.search(fName):
            yield os.path.join(folder,fName)

def make_gazet(fin):
    ftemp = fin+".1col"
    txt1 = getText(fin)
    txt2 = get_columns(txt1,' ', [0])
    writeText(ftemp,txt2)
    f = open(fin+".1col")
    txt3 = f.read();
    fout = open(fin+'.dict','w')
    match = re.sub('\w+','',txt3);
    """match = re.split(r'\w+',txt3)
    for str in match:
        if (str != ''):
            fout.write(str)
    """ 
    match = re.sub('\n+','\n',match);  
    fout.write(match)
    fout.close()
    os.remove(ftemp)
              
if __name__=="__main__":    
    f = os.path.abspath(sys.argv[1])
    if os.path.isfile(f):
        fName = f
       # make_gazet(fName)
        exit()
    
    folder = f
   # print folder
    #for fName in files(folder, "(.*?)\.f$"):
    for fName in files(folder,"(.*?)\.d$"):
        fName = os.path.abspath(fName)
        print fName
        make_gazet(fName)
      #  cleanTempFiles(fName)

