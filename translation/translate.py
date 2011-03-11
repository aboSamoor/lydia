#! /usr/bin/env python

import httplib
import json
import sys, os
import settings
import store
import urllib
import lydia.aner.tools as tools

def googleTran(query, src= 'ar', to= 'en'):
    try:
        c = httplib.HTTPSConnection('www.googleapis.com')
        query = query.encode('utf-8')
        c.request('GET', '/language/translate/v2?key='+settings.key+'&q=+'+query+'&source='+src+'&'+'target='+to)
        d = c.getresponse()
        c.close()
    except:
        tools.print_exception()
        return ''
    if int(d.status) == 200:
        results = json.load(d)
        return results["data"]["translations"][0]["translatedText"]
    else:
        print >> sys.stderr, "Error: "+d.status+" "+d.reason
        return ''


def wikipediaTran():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: $translate.py repository word" 
        sys.exit()
    engine = store.store(tran, os.path.abspath(sys.argv[1]))
    if len(sys.argv[2:] > 10):
        words = [w.decode('utf-8') for w in sys.argv[2:]]
        engine.prepare(words)
    else:
        for w in sys.argv[2:]:
            print w,engine.get(w.decode('utf-8')).encode('utf-8')
    engine.save()
