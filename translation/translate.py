#! /usr/bin/env python

import httplib
import json
import sys, os
import settings
import store
import urllib2
import lydia.aner.tools as tools
import types
import urllib

def googleTran(query, src= 'ar', to= 'en'):
    try:
        c = httplib.HTTPSConnection('www.googleapis.com')
#        c.set_debuglevel(1)
        if type(query) == types.UnicodeType:
            query = query.encode('utf')
        query = urllib2.quote(query)
        url = '/language/translate/v2?key='+settings.key+'&q=+'+query+'&source='+src+'&'+'target='+to
        c.request('GET', url)
        d = c.getresponse()
    except:
        tools.print_exception()
        return ''
    if int(d.status) == 200:
        try:
            results = json.load(d)
            c.close()
            return results["data"]["translations"][0]["translatedText"]
        except:
            tools.print_exception()
            c.close()
            return ''
    else:
        print >> sys.stderr, "Error: "+str(d.status)+" "+str(d.reason)
        c.close()
        return ''


def getWords(stmt):
    words = stmt.split(' ')
    res = []
    abd = unichr(0x0639) + unichr(0x0628) + unichr(0x62f)
    i = 0
    DET = unichr(0x0627) + unichr(0x0644)
    while i < len(words):
        if words[i] == DET:
            i += 1
            if i < len(words):
                res.append(DET+words[i])
                i += 1
        elif words[i] == abd:
            i += 1
            if i < len(words):
                res.append(abd+' '+words[i])
                i+=1
        else:            
            res.append(words[i])
            i += 1
    return res

def wikipediaTran():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: $translate.py repository [word | fileOfWords]" 
        sys.exit()
    engine = store.store(googleTran, os.path.abspath(sys.argv[1]))
    if os.path.isfile(os.path.abspath(sys.argv[2])):
        words = [l.decode('utf-8') for l in open(os.path.abspath(sys.argv[2]),'r').read().splitlines()]
    else:
        words = [w.decode('utf-8') for w in sys.argv[2:]]

    res = []
    for line in words:
        res.extend(getWords(line))
    words = res
    if len(words) > 10:
        engine.prepare(words)
    else:
        for w in words:
            print w.encode('utf-8'),engine.get(w.decode('utf-8')).encode('utf-8')
    engine.save()
