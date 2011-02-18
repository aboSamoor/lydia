#!/usr/bin/env python

import sys
import os
import settings
import re
import pickle
import tools

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

def make_gazet(fin):
    txt1 = getText(fin)
    txt3 = tools.get_columns(txt1,'->', [0])
    txt4 = re.sub('\w+\s*\n','',txt3);
#    txt5 = re.sub('\n+','\n',txt4);  
    writeText(fin+'.dict',txt4)
              
if __name__=="__main__":    
    f = os.path.abspath(sys.argv[1])
    if os.path.isfile(f):
        fName = f
        make_gazet(fName)
        exit()
    
    folder = f
    for fName in tools.files(folder,"(.*?)\.d$"):
        fName = os.path.abspath(fName)
        print fName
        make_gazet(fName)
