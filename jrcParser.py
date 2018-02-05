from sys import argv
import re
import glob
import os

# 1. Library to use
# 2. Language
# 3. Output directory name
def readFile(filename):
    if not os.path.exists(filename):
        return False
    f = open(filename, 'r')
    try:
        content = f.read()
    finally:
        f.close()
    return content

def writeFile(filename,content,append=False):
    if append:
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    try:
        content = f.write(content)
    finally:
        f.close()

def readJRC(filePath, yearOutputDir):
    bodies = re.findall(r'<body>(.*?)</body>',readFile(filePath),flags=re.DOTALL)
    fileName = filePath.split('/')[-1]
    fileName = fileName.split('.')[0]
    print (fileName)
    if not bodies:
        return
    body = bodies[0]
    split = re.split(r'<[^>]*>',body)
    newtext = "\n".join(split)
    newtext = re.sub("\s*\n\s*","\n\n",newtext.strip())
    print (newtext)
    writeFile(yearOutputDir + "/" + fileName + ".txt", newtext, True)

fileDirectory = []
myDir = str(os.getcwd())
fullDir = myDir + '/' + argv[1] + '/' + argv[2]

year = os.listdir(fullDir)
for y in year:
    yearInputDir = fullDir + "/" + str(y)
    yearOutputDir = os.getcwd() + '/' + argv[3] + '/' + argv[2] + '/' + y
    print (yearOutputDir)
    print("\n")
    if not os.path.exists(yearOutputDir):
        os.makedirs(yearOutputDir)
    fileDirectory = glob.glob(yearInputDir + "/*.xml")
    for i in fileDirectory:
        print (i)
        readJRC(i, yearOutputDir)

print (fullDir)

