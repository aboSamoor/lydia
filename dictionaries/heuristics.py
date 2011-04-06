#! /usr/bin/env python 

import os, sys
import lydia.aner.tools as tools
import types
import lydia.aner.csvConverter as csvConverter
import re


def factor(str1, str2):
    if ":" in str1 or ":" in str2:
        return []
    
    if type(str1) == types.StringType:
        str1 = str1.decode('utf-8')
    if type(str2) == types.StringType:
        str2 = str2.decode('utf-8')
    w1 = re.findall(r'\w+', str1, re.U)
    w1 = filter(lambda x: x != 'of', w1)
    w2 = re.findall(r'\w+', str2, re.U)
#    w2.reverse()
    if len(w1) == len(w2):
        return zip(w1,w2)
    return []
    


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print "$bla.py input_csv"
    fName = os.path.abspath(sys.argv[1])
    srcList = csvConverter.csv2dicts(fName)
    resDict = {}
    for item in srcList:
        for pair in factor(item["Arabic"], item["English"]):
            resDict[pair[0]]  = pair[1]
    resDicts = csvConverter.buildListOfDictionaries(resDict, "key")
    csvConverter.dicts2csv(resDicts, fName+".deduced.csv") 

