#! /usr/bin/env python

import os, sys
import tools
import json

postNERHeader = {0: "word", 1: "POS", 2:"POS1", 3:"POS2", 4:"NER"}

def convert(header, f, delim):
    fh = open(f, 'r')
    text = fh.read()
    fh.close()
    result = []
    for line in text.splitlines():
        taggedWords = {}
        words = line.split(delim)
        if len(words) < 2:
            for index in header.keys():
                taggedWords[header[index]] = ''
        else:
            for index in header.keys():
                taggedWords[header[index]] = words[index]
        taggedWords["virtual"] = False
        result.append(taggedWords)
    return result

def print_exception():
    exc_type, exc_value = sys.exc_info()[:2]
    print 'Handling %s exception with message "%s"' % \
        (exc_type.__name__, exc_value)

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "usage : 2json.py fileName"
    f = os.path.abspath(sys.argv[1])
    exts = f.split('.')
    newFile = exts[0] + '.json' 
    if not os.path.isfile(f):
        print  "Error "+f +" file does not exists"
        sys.exit()
    if exts[-1] == "NER":
        if exts[-2] == "post":
            result = convert(postNERHeader, f, '\t')
    else:
        sys.exit()
    fh = open(newFile, 'w')
    try:
        json.dump(result, fh)
    except:
        print "Error "+newFile +" failed to be written"
        print_exception()
        fh.close()
        os.remove(newFile)
        sys.exit()
    fh.close()
