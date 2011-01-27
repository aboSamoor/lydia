#!/usr/bin/env python

import sys
import os
import settings

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

def oneCol(fin, fout):
    text = open(fin, 'r').read()
    filp = open(fout, 'w')
    for line in text.splitlines():
        for word in line.split(' '):
            filp.write(word+"\n")
    filp.close()

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
    fh = open(fin, 'r')
    text = fh.read()
    fh.close()
    return text

def writeText(fout, text):
    fh = open(fout, 'w')
    text = fh.write(text)
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
    
    txt1 = getText(fin+".bw.TOK.NORM.posOut")
    txt2 = get_columns(txt1, '\t', [0,1,10,11])
    fPre = fin+".bw.pre.NER"
    writeText(fPre, txt2)

    fAfter = fin + ".bw.post.NER"
    yamcha(fPre, fAfter, settings.amira_dir+"/SVMmodel.model")

    txt3 = getText(fAfter)
    txt4 = get_columns(txt3, '\t', [0,4])
    writeText(fin+".bw.ner", txt4)

if __name__=="__main__":
    amira_dir = settings.amira_dir
    fin = os.path.abspath(sys.argv[1])
    ner(fin)
    bwtoutf8(fin+".bw.ner",fin+".ner") 
    
