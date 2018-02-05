# -*- coding: cp1252 -*-

import os
import re
import random
import heapq
from sys import argv
import codecs
import glob
# 1. Europarl Original Folder
# 2. Output folder name
# 3. Language that needs to be extracted

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def readFile(filename):
    if not os.path.exists(filename):
        return False
    f = codecs.open(filename, encoding = 'ISO-8859-1', errors= 'ignore')
    try:
        content = f.read()
    finally:
        f.close()
    return content

def writeFile(filename,content,append=False,overwrite=False):
    ensure_dir(filename)
    if append:
        f = codecs.open(filename, 'a', 'utf-8')
    else:
        f = codecs.open(filename, 'w', 'utf-8')
    try:
        content = f.write(content)
    finally:
        f.close()


def addPunctuation(matchobj):
    return matchobj.group(0).replace('\n', '') + '.\n'


def readOneFile(filePath, lang):
    content = readFile(filePath)
    fileName = filePath.split('/')[-1]

    matches = re.findall(r'ID="?([0-9]+)"?[^>]*LANGUAGE="(DA|DE|EN|ES|FR|IT|PT|SV)"[^>]*>(.+?)(<SPEAKER|<CHAPTER|\Z)',content,flags=re.DOTALL)
    
    year = fileName[3:5]
    propername = fileName[:-4]

    temp = re.sub(r'<.*?>','', content, flags=re.DOTALL)
    temp = re.sub(r'[0-9a-z)})%]\n', addPunctuation, temp, flags=re.DOTALL) # Add punctuation if not punctuated
    temp.encode('utf-8')
    newname = os.path.join(os.getcwd(), argv[2], lang, fileName)
    writeFile(newname, temp,True)


def main():
    
    for i in range (3, len(argv)):
    
        fileDirectory = glob.glob(os.path.join(os.getcwd(), argv[1], argv[i], "*.txt"))
        for file in fileDirectory:
            readOneFile(file, argv[i])
if __name__ == "__main__":
    main()
