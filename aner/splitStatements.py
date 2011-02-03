import NER
import sys
import os
import re

if __name__=="__main__":
    fin = os.path.abspath(sys.argv[1])
    fout = os.path.abspath(sys.argv[2])
    text = NER.getText(fin)
    txt = re.sub(r"([.|?|!]\tO)",'\\1\n',text)
    NER.writeText(fout, txt)
