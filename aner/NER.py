#!/usr/bin/env python

import sys
import os
import settings
import re
import pickle
import tools

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
    text = fh.write(text)
    fh.close()
    


def ner(fin):
    AMIRA(fin)
    txt1 = getText(fin+".bw.TOK.NORM.POS.bpcOut")
    print "Preparing data for NER"
    txt2 = tools.get_columns(txt1, '\t', [0,1,10,11])
    fPre = fin+".bw.pre.NER"
    writeText(fPre, txt2)
    fAfter = fin + ".bw.post.NER"
    print "Runnin yamcha for NER"
    yamcha(fPre, fAfter, settings.amira_dir+"/SVMmodel.model")

    txt3 = getText(fAfter)
    print "Producing formatted NER output"
    txt4 = tools.get_columns(txt3, '\t', [0,4])
    writeText(fin+".bw.ner", txt4)
    print ""

        
def cleanTempFiles(fin):
        fin = os.path.abspath(fin)
        exts = ['.amirabpc', '.amirapos', '.amiratok', '.bw.ner', '.bw.pre.NER', '.bw.TOK.NORM.POS.bpcOut', '.bw.TOK.NORM.posOut']
        for i in exts:
            if os.path.isfile(fin+i):
                os.remove(fin+i)
            else:
                print fin+i,"does not exists"
            

if __name__=="__main__":
    amira_dir = settings.amira_dir
    results = {}

    f = os.path.abspath(sys.argv[1])

    if os.path.isfile(f):
        fName = f
        ner(fName)
        exit()

    folder = f
    for fName in tools.files(folder, "(.*?)\.f$"):
        fName = os.path.abspath(fName)
        print fName
        ner(fName)
        partial = parsePostNER(fName+".bw.post.NER")
        add2Results(partial, results)
        cleanTempFiles(fName)
    statFile = os.path.join(folder, 'stats')
    fh = open(statFile,'w')
    print results
    pickle.dump(results,fh)
    fh.close()
