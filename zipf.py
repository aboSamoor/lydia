#! /usr/bin/env python

import random
import matplotlib.pyplot as plt

def pick_char(l):
    return l[random.randint(0,len(l)-1)]

def init():
    alphabet = [chr(i) for i in range(0x61,0x7B)]
    alphabet.append(chr(0x20))
    return alphabet
    
def tuples2lists(l_tuples):
    size_tuple = len(l_tuples[0])
    l_lists = []
    for i in range(size_tuple):
        l_lists.append([])
    for point in l_tuples:
        for i in range(size_tuple):
            l_lists[i].append(point[i])
    return l_lists

def fill(num):
    alphabet = init()
    chars = [pick_char(alphabet) for i in range(num)]
    text = ''.join(chars)
    return text

def stats(text):
    dictionary = {}
    for word in text.split(' '):
        if not dictionary.has_key(word):
            dictionary[word] = 0
        dictionary[word] +=1

    results = []
    for word in dictionary.keys():
        results.append((dictionary[word],word))

    results.sort()
    return results

if __name__=="__main__":
    text = fill(100000000)
    results = stats(text)
    l_lists = tuples2lists(results)
    frequency = l_lists[0]
    print frequency
    frequency.reverse()
    plt.loglog(frequency)
    plt.show()
