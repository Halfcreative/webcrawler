#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
swFilter = True
stem = True
swList = open('sw.txt', 'r').read()

def prep(str):
    words = str.lower().split()
    
    if swFilter:
        for i in range(len(words)):
            if words[i] in swList:
               words[i] = '<sw>'
               
    words = list(filter(lambda x: x != '<sw>', words))

    if stem:
        for i in range(len(words)):
            words[i] = stem(words[i])

    return words

def stem(word):
    #suffix-stripping:
    word = re.sub(r's$', '', word)
    word = re.sub(r'ed', '', word)
    word = re.sub(r'([^i]ly$)|(ily$)', '', word)
    word = re.sub(r'ing$', '', word)
    word = re.sub(r"\'\w*$", '', word) #an apostrophe and anything after it
    return word
    

def main():
    strIn = input('enter some stuff:\t')
    oot = prep(strIn)
    print(' '.join(oot))
    
main()