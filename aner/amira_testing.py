#!/usr/bin/env python

import sys
import os
import re
import time
import math
import random



def gettext(fName):
    fHandler = open(fName,'r')
    text = fHandler.read()
    fHandler.close()
    return text

def search(fName, pattern):
    results=re.findall(pattern, gettext(fName))
    return len(results) 

def run(prog, config, fName):
    amira_dir_bin = os.path.dirname(prog)
    amira_dir = os.path.dirname(amira_dir_bin)
    executable = os.path.basename(prog)

    config_path= "../configs/"+config
    current = os.path.abspath(os.path.curdir)
    os.chdir(amira_dir_bin)
    cmd = "perl " + executable  + " config="+ config_path +" file="+fName
    print cmd
    before = time.time()
    os.system(cmd)
    after = time.time()
    os.chdir(current)
    return after-before

def batch(prog, config, fName, times):
    results = []
    source = unicode(gettext(fName), "utf-8")
    length = len(source)
    inc = 1.25
    tmp = "/tmp/partial"
    sizes = [int(10*(inc**i)) for i in range(int(math.log(length/10.0,inc)))]
#   sizes.reverse()
#   sizes = [1000,2000,4000]
    for i in sizes:
        for j in range(times):
            index = random.randint(0,length-i)
            open(tmp,'w').write(source[index:index+i].encode("utf-8"))
            time = run(prog, config, tmp)
            results.append((i,time))
            print results[-1]
    return results
            
    
    

if __name__=="__main__":
    res=str(batch(sys.argv[1], sys.argv[2], sys.argv[3], 6))
    print res
    open('results','w').write(res)
