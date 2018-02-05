# -*- coding: cp1252 -*-

import os
import re
import random
import heapq
from sys import argv

import glob
# 1. Location of the Europarl Text
# 2. language
# 3. output folder

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def readFile(filename):
    if not os.path.exists(filename):
        return False
    f = open(filename, 'r')
    try:
        content = f.read()
    finally:
        f.close()
    return content

def writeFile(filename,content,append=False,overwrite=False):
    ensure_dir(filename)
    if append:
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    try:
        content = f.write(content)
    finally:
        f.close()

def listFiles(dir, list):

    for item in os.listdir(dir):
        #print item
        list.append(item)

def allFiles(dir, list):
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if name[-3:] == "txt":
                list.append(os.path.join(path,name))

def extract(language):
    filenames = []
    listFiles(language, filenames)
    # print (filenames)
    # print(language)
    for fn in filenames:
        findSpeech(language,fn)

def findSpeech(language, filename):
    path = "Extracted" + os.sep
    content = readFile(language + os.sep + filename)
    #print(content)
    #matches = re.findall(r'ID="?([0-9]+)"?[^>]*LANGUAGE="(DA|DE|EN|ES|FR|IT|PT|SV)"[^>]*>(.+?)(<SPEAKER|<CHAPTER|\Z)',content,flags=re.DOTALL)
    matches = re.findall(r'ID="?([0-9]+)"?[^>]*>(.+?)(<SPEAKER|<CHAPTER|\Z)',content,flags=re.DOTALL)

    year = filename[3:5]
    propername = filename[:-4]
    #print(matches)
    for m in matches:
        lang = m[1].lower()
        newname = path + lang + os.sep + year + os.sep + propername + "-" + m[0] + ".txt"
	#print(newname)
        if not os.path.exists(newname):
            source = readFile(lang + os.sep + filename)
            if source:
                text = re.findall(r'SPEAKER ID="?'+m[0]+r'"?( [^>]*>|>)(.+?)(<SPEAKER|<CHAPTER|\Z)',source,flags=re.DOTALL)
                if text:
                    writeFile(newname,text[0][1])

def select(language, number):
    filenames = []
    allFiles("Extracted" + os.sep + language, filenames)
    c=0
    while(True):
        r = random.randint(0,len(filenames)-1)
        chosen = filenames[r]
        del filenames[r]
        content = readFile(chosen)
        if re.search("\S",content):
            writeFile(re.sub("Extracted","Selected",chosen), content)
            c += 1
        if c == number:
            break

def clean(language):
    filenames = []
    allFiles("Selected" + os.sep + language,filenames)
    for fn in filenames:
        cleanEuroparl(fn)

def cleanEuroparl(filename):
    body = readFile(filename)
    split = re.split(r'<[^>]*>',body)
    newtext = "\n".join(split)
    newtext = re.findall(u'(?us)(Â|\s|\W)*(\w.*)',newtext)[0][1]
    newtext = re.sub("\s*\n\s*","\n\n",newtext.strip())
    writeFile(re.sub("Selected", "Cleaned", filename), newtext)

    #writeFile(re.sub("Selected","Cleaned",filename), newtext)

def dashrepl(matchobj):
    print (matchobj.group(0).replace('\n', ''))
    return matchobj.group(0).replace('\n', '') + '.\n'

def readOneFile(filePath):
    content = readFile(filePath)
    fileName = filePath.split('/')[-1]
    print argv[2]

    #matches = re.findall(r'ID="?([0-9]+)"?[^>]*LANGUAGE="(DA|DE|EN|ES|FR|IT|PT|SV)"[^>]*>(.+?)(<SPEAKER|<CHAPTER|\Z)',content,flags=re.DOTALL)
    #matches = re.findall(r'ID="?([0-9]+)"?[^>]*>(.+?)(<SPEAKER|<CHAPTER|\Z)',content,flags=re.DOTALL)

    matches = re.findall(r'ID="?([0-9]+)"?[^>]*>(.+?)(<SPEAKER|\Z)', content, flags=re.DOTALL)
    print ("MATCHES ARE")
    print matches
    print ("END OF MATCHES")
    year = fileName[3:5]
    propername = fileName[:-4]
    #print(matches)
    print ("TEST")
    print year
    print propername

    for m in matches:
        lang = m[1].lower()
        # print ("Test m")
        # print (m[1])
        # print("\n")
        #temp = m[1].replace("<P>", "")
        temp = re.sub(r'<.*?>', '', m[1], flags=re.DOTALL)
        #temp = temp.replace('^< >$', '')
        temp = re.sub(r'[a-z)})]\n', dashrepl, temp, flags=re.DOTALL)
        #temp = temp.replace(r'^< >$', '')

        print ("Test!")
        print temp
        newname = os.getcwd() + '/' + argv[3] +'/' + argv[2] + '/' + fileName
        writeFile(newname, temp,True)
        #print(newname)
        # source = readFile(filePath)
        # if source:
        #     text = re.findall(r'SPEAKER ID="?'+m[0]+r'"?( [^>]*>|>)(.+?)(<SPEAKER|CHAPTER|\Z)',source,flags=re.DOTALL)
        #     print ("Text is here")
        #     print (text)
        #     print m
        #     print ('\n')
        #     if text:
        #         writeFile(newname,text[0][1], True)

print (os.getcwd() + '/' + argv[1] + '/' + argv[2])
fileDirectory = glob.glob(os.getcwd() + '/' + argv[1] + '/' + argv[2] + "/*.txt")
#print fileDirectory
for i in fileDirectory:
    readOneFile(i)
    #print (i)
    #print('\n')
    #cleanEuroparl(i)
