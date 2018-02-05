from __future__ import division, unicode_literals
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import Text

genreList = [u'adventure', u'belles_lettres', u'editorial', u'fiction', u'government', u'hobbies', u'humor', u'learned', u'lore', u'mystery', u'news', u'religion', u'reviews', u'romance', u'science_fiction']
import os
import csv
from sys import argv
import re
import numpy as np
from textblob import TextBlob as tb
import math
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import string
from nltk import word_tokenize

# 1. directory of extracting
# 2. output location
# 3. output filename


# Find the word frequencies in all the texts in corpora(ratio)
# Find the word frequency in the text (ratio)
# Multiply them
mapFeatures = {}
title = ['ID','File Name', 'Single Sentence Paragraph Count', 'Single sentence paragraph/ sentence ratio',
         'Paragraph Length Mean', 'Closing parenthesis frequency',
         'Opening Parenthesis Frequency', 'Number frequency',
         'Forward slash frequency', 'Single sentence distribution value',
         'Colon frequency', 'Sentence length mean', 'Top 10 tf-idf average precision','Type/token ratio',
         'Document Length', 'Paragraph Length STD', 'Hyphen Frequency']

def countExists(numCount, symbol, words):
    if (symbol in words):
        numCount += 1
    return numCount

my_sent_tokenizer = nltk.RegexpTokenizer('[^.!?]+')
#corpus1 = PlaintextCorpusReader(os.getcwd() + '/' + argv[1], '.*txt', sent_tokenizer=my_sent_tokenizer)

corpus1 = PlaintextCorpusReader(os.getcwd() + '/' + argv[1], '.*txt')
outputFile = open(os.getcwd() + '/' + argv[2] + '/' + argv[3], 'w')
output_writer = csv.writer(outputFile)
output_writer.writerow(title)

totalWords = corpus1.words()
distinct = {}

countDocument = 0
for w in totalWords:
    if w in distinct:
        distinct[w] += 1
    else:
        distinct[w] = 1

for j in distinct.keys():
    distinct[j] = distinct[j] / len(totalWords)


for i in corpus1.fileids():
    countDocument += 1
    totalWordLength = 0.0
    totalSentLength = 0.0
    maxSentLength = 0.0
    meanSentLength = 0.0
    avgParagraphLength = 0.0
    numParagraphs = 0.0
    numwords = 0.0
    numNumber = 0.0

    print ("Percentage of completion")
    print (countDocument / float(len(corpus1.fileids())))
    paraLengthMean = 0.0
    distinctWordList = []

    numOpenParantheses = 0.0
    numClosedParantheses = 0.0
    avgOpenParantheses = 0.0
    avgClosedParantheses = 0.0

    numForwardSlash = 0.0
    numColon = 0.0
    numHyphen = 0
    numQuotation = 0
    corpus0 = PlaintextCorpusReader(os.getcwd() + '/' + argv[1] + '/', i)
    words = corpus0.words()
    sentences = corpus0.sents()
    paras = corpus0.paras()

    numWords = len(corpus0.words())
    numParagraphs = len(paras)

    numSingleSentPara = 0
    paraLengthList = []
    listUniCodeChar = u'.!?;'
    middleDocument = float (len(sentences)/ 2)
    singleSentDistributionArray = []
    sentLocation = 0
    tfidfList = []

    wordFreq = {}
    for p in paras:
        sentCount = 0
        #List of words in each paragraph
        for word in p:

            #Go through each word
            for w in word:
                if (w in listUniCodeChar):
                    sentCount +=1
                    sentLocation +=1

            if (sentCount == 1):
                numSingleSentPara +=1
                singleSentDistributionArray.append((sentLocation-middleDocument))

        paraLengthList.append(len(p))

    avgSingleSentDist = np.mean(singleSentDistributionArray)
    ratioSingleSentPara= numSingleSentPara/len(sentences)
    if (len(paraLengthList) > 1):
        stdParaLength = np.std(paraLengthList, ddof = 1)
    else:
        stdParaLength = 0

    for sent in sentences:
        totalSentLength += len(sent)
        if (len(sent) > maxSentLength):
            maxSentLength = len(sent)
    meanSentLength = totalSentLength / len(sentences)
    print (totalSentLength)
    print ("Mean")
    print (meanSentLength)
    print (len(sentences))
    for word in words:
        word = word.lower()

        if not (word in distinctWordList):
            distinctWordList.append(word)
        if (word in wordFreq):
            wordFreq[word] +=1
        else:
            wordFreq [word] = 1

        numClosedParantheses = countExists(numOpenParantheses, '(', word)
        numClosedParantheses = countExists(numClosedParantheses, ')', word)
        numHyphen = countExists(numHyphen, '-', word)
        numForwardSlash = countExists(numForwardSlash,'/', word)
        numColon = countExists(numColon, ':', word)
        if(word.isdigit()):
            numNumber += 1

        totalWordLength = totalWordLength + len(word)

    for wo in wordFreq.keys():
        wordFreq[wo] = wordFreq[wo] / len (words)

    for wo in wordFreq.keys():
        if (wo in distinct) and (distinct[wo] != 0.0):
            currenttfidf = wordFreq[wo] * distinct[wo]
            tfidfList.append(currenttfidf)
    tfidfList.sort(reverse=True)
    averagetfidf = np.mean(tfidfList[0:9])
    typeRatio = len(distinctWordList) / numWords

    print ("TF_IDF")
    print(averagetfidf)

    paraLengthMean = totalWordLength / numParagraphs
    mapFeatures[i] = [countDocument, numSingleSentPara, ratioSingleSentPara, paraLengthMean,
                      numClosedParantheses,numOpenParantheses, numNumber,
                      numForwardSlash, avgSingleSentDist, numColon, meanSentLength,
                      typeRatio, averagetfidf, numWords, stdParaLength, numHyphen]

    output_writer.writerow([countDocument, i,numSingleSentPara, ratioSingleSentPara, paraLengthMean,
                            numClosedParantheses, numOpenParantheses, numNumber,
                            numForwardSlash, avgSingleSentDist, numColon, meanSentLength, typeRatio,
                            averagetfidf, numWords, stdParaLength, numHyphen])



