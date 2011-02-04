#!/usr/bin/env python

import sys
import os
import settings
import re
import pickle


def utf8tobw(fin,fout):
    amira_dir = settings.amira_dir
    cmd = "cat "+fin+" | perl clean-utf8.pl clean-utf8-MAP | perl ArabicTokenizer.pl UTF-8 BUCKWALTER notokenization > "+fout
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir+"/bin")
    os.system(cmd) 
    os.chdir(current)

def bwtoutf8(fin,fout):
    amira_dir = settings.amira_dir
    cmd = "cat "+fin+" | perl clean-utf8.pl clean-utf8-MAP | perl ArabicTokenizer.pl BUCKWALTER UTF-8 notokenization > "+fout
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir+"/bin")
    os.system(cmd) 
    os.chdir(current)

def tokenize(fName, amira_dir):
    cmd="perl AMIRA.pl config=../configs/tok_only.amiraconfig file="+fName
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir+"/bin")
    os.system(cmd) 
    os.chdir(current)

def tok_pos(fName, amira_dir):
    cmd="perl AMIRA.pl config=../configs/tok_pos.amiraconfig file="+fName
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir+"/bin")
    os.system(cmd) 
    os.chdir(current)

def yamcha(fin, fout, model):
    cmd = ''.join(["yamcha ", '-m ', model, ' <', fin, '> ', fout])
    os.system(cmd)

def AMIRA(fin):
    amira_dir = settings.amira_dir
    cmd = "perl AMIRA.pl config=../configs/all.amiraconfig file="+fin
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir+"/bin")
    os.system(cmd) 
    os.chdir(current)

def getText(fin):
    fin = os.path.abspath(fin)
    fh = open(fin, 'r')
    text = fh.read()
    fh.close()
    return text

def writeText(fout, text):
    fout = os.path.abspath(fout)
    fh = open(fout, 'w')
    text = fh.write(text.encode('utf-8'))
    fh.close()
    

def get_columns(text, delimiter, cols):
    result = []
    for line in text.splitlines():
        if line != '':
            templine = line.split(delimiter)    
            newline = [templine[j] for j in cols]
            result.append(delimiter.join(newline))
        else:
            result.append(line)
    return '\n'.join(result)

def ner(fin):
    AMIRA(fin) 
    txt1 = getText(fin+".bw.TOK.NORM.POS.bpcOut")
    txt2 = get_columns(txt1, '\t', [0,1,10,11])
    fPre = fin+".bw.pre.NER"
    writeText(fPre, txt2)

    fAfter = fin + ".bw.post.NER"
    yamcha(fPre, fAfter, settings.amira_dir+"/SVMmodel.model")

    txt3 = getText(fAfter)
    txt4 = get_columns(txt3, '\t', [0,4])
    writeText(fin+".bw.ner", txt4)

def parsePostNER(fin):
    statistics = {}
    text = getText(fin)
    for line in text.splitlines():
        if line != '':
            cols = [word for word in line.split('\t')]
            if  len(cols) != 5:
                print line
                print "not well formatted line"
                continue
            else:
                if cols[1] == 'NNP':
                    if not statistics.has_key(cols[0]):
                        statistics[cols[0]] = {}
                    if not statistics[cols[0]].has_key(cols[4]):
                            statistics[cols[0]][cols[4]]=0
                    statistics[cols[0]][cols[4]] += 1
    return statistics
        
def cleanTempFiles(fin):
        fin = os.path.abspath(fin)
        exts = ['.amirabpc', '.amirapos', '.amiratok', '.bw.ner', '.bw.pre.NER', '.bw.TOK.NORM.POS.bpcOut', '.bw.TOK.NORM.posOut']
        for i in exts:
            os.remove(fin+i)


def files(folder, pattern):
    folder = os.path.abspath(folder)
    ptrn = re.compile(pattern)
    if not os.path.isdir(folder):
        print "this is a file"
        yield ''
    for fName in os.listdir(folder):
        if ptrn.search(fName):
            yield os.path.join(folder,fName)

def add2Results(partial, store):
    for k in partial.keys():
        for v in partial[k].keys():
            if not store.has_key(k):
                store[k] = {}
            if not store[k].has_key(v):
                store[k][v] = 0
            store[k][v] += 1
    return store

            

if __name__=="__main__":
    amira_dir = settings.amira_dir
    results = {}

    f = os.path.abspath(sys.argv[1])

    if os.path.isfile(f):
        fName = f
        ner(fName)
        exit()

    folder = f
    for fName in files(folder, ".*?.f"):
        fName = os.path.abspath(fName)
        print fName
        ner(fName)
        partial = parsePostNER(fName+".bw.post.NER")
        add2Results(partial, results)
        cleanTempFiles(fName)
    fh = open('/home/eid/Desktop/stats','w')
    print results
    pickle.dump(results,fh)
    fh.close()
