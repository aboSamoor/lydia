import NER
import sys
import os

if __name__=="__main__":
    fin = os.path.abspath(sys.argv[1])
    fout = os.path.abspath(sys.argv[2])
    text = NER.getText(fin)
    NER.writeText(fout, '.\tO\n'.join([stmt for stmt in text.split('.\tO')]))

#    for line in text.splitlines():
#        if line[0] == '.':
#            result+ = '\n'
#        result += line
    
