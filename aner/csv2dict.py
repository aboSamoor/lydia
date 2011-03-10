#! /usr/bin/env python

import csv
import sys, os
import tools

def convert(fName, fieldNames=[]):
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
    result = buildDictionary(convert(fName),"key")
    newFile = fName.split(os.path.extsep)[0]+".json"
    tools.dumpJson(result, newFile)
