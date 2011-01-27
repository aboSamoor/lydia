#!/usr/bin/env python

from parser import subTree
import xml.sax
import sys
import os
import re

outputPath = ""

def op2(text):
    print re.findall(r'<title>(.*?)</title>',text)[0].encode("utf-8")

#parser2 = xml.sax.make_parser()
#contentHandler = subTree("title", op2)
#parser2.setContentHandler(contentHandler)

def generateNewXML(text):
    text = '<?xml version="1.0" encoding="utf-8"?>'+ text 
    text = text.encode("utf-8")
    m = re.search('<id>(.*?)</id>', text)
    if m:
        fName = outputPath+"/"+m.group(1)
        print fName 
        open(fName,'w').write(text)
#    xml.sax.parseString(text, contentHandler)
#    tmpFile ="/tmp/_987654321.xml"
#    tmpHandler = open(tmpFile,'w')
#    tmpHandler.write(text2.encode("utf-8"))
#    tmpHandler.close()
#    tmpHandler2 = open(tmpFile, 'r')
#    parser2.parse(tmpHandler2)
#    tmpHandler2.close()
    
def puts(text):
    print text


if __name__=="__main__":
    if len(sys.argv) < 3:
        print "Usage: $fragmenter.py wikipediaDump outputDirectory"
        sys.exit()
    outputPath = sys.argv[2]
    parser = xml.sax.make_parser()
    parser.setContentHandler(subTree("page", generateNewXML))
    parser.parse(open(sys.argv[1],"r"))
