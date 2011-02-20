#! /usr/bin/env python

import json
import os

class store():
    def __init__(self, func, fName):
        self.op = func
        self.file = os.path.abspath(fName)
        if os.path.isfile(self.file):
            try:
                self.dictionary = json.load(open(fName, 'r'))
                print "Dictionary loaded"
            except:
                print "failed to parse the file"
                self.file = os.path.abspath(fName+".tmp")
                fh = open(self.file, 'w')
                fh.close()
                self.dictionary = {}
        else:
            fh = open(fName, 'w')
            fh.close()
            self.dictionary = {}

    def get(self, item):
        if not self.dictionary.has_key(item):
            res = self.op(item)
            if res:
                self.dictionary[item]= res
                return self.dictionary[item]
            else:
                return ''

    def save(self):
        fh = open(self.file, 'w')
        json.dump(self.dictionary, fh)
        fh.close()
