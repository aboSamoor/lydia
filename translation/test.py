#! /usr/bin/env python

import store

def op(i):
    print i
    return str(int(i)+1)

if __name__=="__main__":
    
    bla = store.store(op,'repo')
    for i in range(10):
        bla.get(str(i))
    for i in range(10):
        bla.get(str(i))
    bla.save()
