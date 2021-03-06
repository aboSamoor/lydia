#! /usr/bin/env python
import os, sys
import tools

def getTags(store):
    b=set()
    for k in store.keys():
        for v in store[k].keys():
            b.add(v)
    return list(b)


class record():
    def __init__(self, dictionary, word):
        self.tags = {'I-FAC':0, 'I-LOC':1, 'B-ORG':2, 'O':3, 'B-PER':4, 'I-PER':5, 'B-FAC':6, 'I-ORG':7, 'B-LOC':8, 'PER':9, 'LOC':10, 'ORG':11}
        self.freqs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in dictionary.keys():
            self.freqs[self.tags[k]] = dictionary[k]
            self.word = word
    def __str__(self):
        return self.word+','+','.join([str(i) for i in self.freqs])

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "usage: stat2csv.py fileName\n the file should in json format"
    f = os.path.abspath(sys.argv[1])
    store = tools.loadJson(f)
    if store == -1:
        sys.exit()
    records = []
    for k in store.keys():
        records.append(record(store[k],k))
    text  = [str(rec) for rec in records]
    tools.writeText(f+'.csv','\n'.join(text)) 
    
