#! /usr/bin/env python

import json
import os
import Queue
import threading

class store():
    def __init__(self, func, fName):
        self.op = func
        self.file = os.path.abspath(fName)
        self.q = Queue.Queue()
        self.numOfWorkers = 10
        self.lock = threading.Lock()
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
                self.lock.acquire()
                self.dictionary[item]= res
                self.lock.release()
            else:
                return ''
        return self.dictionary[item]            

    def save(self):
        print "File saved and the remaining items are: ", self.q.qsize()
        fh = open(self.file, 'w')
        self.lock.acquire()
        try:
            json.dump(self.dictionary, fh)
            self.lock.release()
            fh.close()
        except:
            self.lock.release()
            fh.close()
    
    def worker(self):
        while True:
            item = self.q.get()
            res = self.get(item)
            print self.q.qsize(),threading.activeCount(),threading.current_thread().name, item, res
            self.q.task_done()
            if self.q.qsize()%100 == 0 and self.q.qsize() != 0:
                self.save()

    def prepare(self, items):
        for e in items:
            self.q.put(e)
        for i in range(self.numOfWorkers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
        self.q.join()
        self.save()
