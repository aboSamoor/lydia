#! /usr/bin/env python

import csv
import sys, os
import tools
import cStringIO
import codecs
import types

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8",fieldnames =[], **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.fieldNames = fieldnames

    def writerow(self, row):
        tmp = []
        for s in row:
            if type(s) == types.UnicodeType:
                tmp.append(s.encode('utf-8'))
            else:
                tmp.append(s)
        self.writer.writerow(tmp)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writeDict(self, Dict):
        self.writerow([Dict[k] for k in self.fieldNames])

    def writeDicts(self, Dicts):
        if not self.fieldNames:
            print "No valid Field Names assigned"
            sys.exit()
        for Dict in Dicts:
            self.writeDict(Dict)


def csv2dicts(fName, fieldNames=[]):
    # detect dialect
    fh = open(fName,'rb')
    csvDialect = csv.Sniffer().sniff(fh.read(1024))
    fh.seek(0)
    #detect any possible headers, otherwise you should supply the header
    if not fieldNames:
        headerReader = csv.reader(fh, dialect = csvDialect)
        fieldNames = headerReader.next()
        fh.seek(0)
    #start parsing
    dictReader = csv.DictReader(fh, dialect = csvDialect, fieldnames = fieldNames)
    result = []
    for row in dictReader:
        result.append(row)
    fh.close()
    return result

def dicts2csv(listOfDicts, fName):
    fh = open(fName, 'w')
    csvWriter = UnicodeWriter(fh,fieldnames=listOfDicts[0].keys())
    csvWriter.writeDicts(listOfDicts)
    fh.close()
 
def buildDictionary(listOfDicts, key):
    dictionary = {}
    for e in listOfDicts:
        keyWord = e[key]
        dictionary[keyWord] = e
        del dictionary[keyWord][key]
    return dictionary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: $csv2json filename\ncsv file should contain the columns header in the first row, the first column will be considered as a key value\n the result will be a json dictionary"
        sys.exit()
    fName = os.path.abspath(sys.argv[1])
#    result = buildDictionary(convert(fName),"key")
    result = csv2dicts(fName)
    newFile = fName.split(os.path.extsep)[0]+".json"
    tools.dumpJson(result, newFile)
