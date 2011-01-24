#!/usr/bin/env python

import sys
import os

def utf8tobw(fin,fout,amira_dir):
    cmd = "cat "+fin+" | perl clean-utf8.pl clean-utf8-MAP | perl ArabicTokenizer.pl UTF-8 BUCKWALTER notokenization > "+fout
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
    cmd = ' '.join(["yamcha", '-m', model, '<', fin, '>', fout])
    os.system(cmd)

if __name__=="__main__":
    amira_dir = sys.argv[1]
    fin = sys.argv[2]
#   model = sys.argv[3]
    
    fin_bw = fin+".bw"
    fin_tok = fin+".amiratok"
    fin_tokOut = fin+".bw.tokOut"
    fin_bw1 = fin_bw+"1"
    result  = fin+".res"
    fin_tmp = fin+".bw.TOK.NORM.posOut"
    
    utf8tobw(fin, fin+".bw", amira_dir)
#   tok_pos(fin, amira_dir)
#   yamcha(fin_tmp, result, model)
