import NER
import sys
import os

if __name__=="__main__":
    fin = os.path.abspath(sys.argv[1])
    fout = os.path.abspath(sys.argv[2])
    NER.utf8tobw(fin,fout)
