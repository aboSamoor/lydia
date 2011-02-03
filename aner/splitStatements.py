#! /usr/bin/env python

import NER
import sys
import os
import re


def fixCols(fin, fout):
    fin = os.path.abspath(fin)
    fout = os.path.abspath(fout)
    text = NER.getText(fin)
    txt = re.sub(r"(\nO)",'\n.\tO',text)
    NER.writeText(fout, txt)

def addNewlines(fin, fout):
    fin = os.path.abspath(fin)
    fout = os.path.abspath(fout)
    text = NER.getText(fin)
    txt = re.sub(r"([.|?|!]\s*O)",'\\1\n',text)
    NER.writeText(fout, txt)

if __name__=="__main__":
    fixCols(sys.argv[1], sys.argv[2])
    addNewlines(sys.argv[2],sys.argv[2]+".out")
