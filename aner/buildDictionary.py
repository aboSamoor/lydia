#! /usr/bin/env python


import os
import sys
import pickle

def add(dic, txt, tag):
    for line in txt.splitlines():
        words = line.split(' ')
        if not dic.has_key(words[0]):
            dic[words[0]] = set([tag])
        else:
            dic[words[0]].add(tag)
            

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "usage : $./buildDictionary currentDictionary NewData DataTag\nExample: $buildDictionary ./store ./cities 'loc'"
        sys.exit()
    gazetteer = os.path.abspath(sys.argv[1])
    data = os.path.abspath(sys.argv[2])
    tag = os.path.abspath(sys.argv[3])

    if not os.path.isfile(gazetteer):
        dic = {}
    else:
        fh = open(gazetteer, 'r')
        dic = pickle.load(fh)
        fh.close()
    txt = open(data, 'r').read()
    add(dic, txt, tag)
    fh = open(gazetteer, 'w')
    pickle.dump(dic, fh)
    fh.close()
