#! /usr/bin/env python


import os
import sys
import pickle

# We are adding only the first part of the name, for example, red sea, we are considering only sea. This works fine with persons name but not with others ;)
def add(dic, txt, tag):
    for line in txt.splitlines():
        words = line.split(' ')
        new = [' '.join(words), words[0]]
        if len(words) > 1:
            new.append(words[1])
        for word in new:
            if word[:2] == 'Al':
                new.append(word[2:])

        for word in new:
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
    tag = sys.argv[3]

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
