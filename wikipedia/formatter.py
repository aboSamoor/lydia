#! /usr/bin/env python

from parser import subTree
import parser
import mwlib.uparser as mwp
import sys, os, re
import xml.sax
from xml.sax.saxutils import unescape
import doStrip

txt = ""
Input = sys.argv[1]
currentFile = ""

def process(text):
    txt = parser.rmExTags(text)
    txt1 = doStrip.dewikify(txt)
    print currentFile
    open(currentFile+".f",'w').write(txt1.encode('utf-8'))

def articles(dir):
    for f in os.listdir(dir):
        f = os.path.join(dir,f)
        if os.path.isfile(f):
            txt = open(f,'rb').read()
            m = re.search('<title>(.*?)</title>',txt)
            if m:
                title = m.group(1)
                if ':' not in title:
                    yield f

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Usage: $formatter.py File"
        print "Usage: $formatter.py Direcotory"
        sys.exit()
    p = xml.sax.make_parser()
    contentHandler = subTree("text", process)
    p.setContentHandler(contentHandler)
    if os.path.isfile(Input):
        currentFile = Input
        fh = open(Input,'r')
        p.parse(fh)
        fh.close()
    else:
        Input = os.path.abspath(Input)
        for f in articles(Input):
            print f
            currentFile = f
            fh = open(f,'r')
            p.parse(fh)
            fh.close()
