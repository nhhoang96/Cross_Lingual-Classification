from __future__ import division, unicode_literals
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import Text

import os
import os.path
import csv
import pandas as pd
from sys import argv
import re
import numpy as np
import math
#from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import string
from nltk import word_tokenize
import time

# 1. Corpus name (Location of the corpus)
# 2. output location
# 3. Languages

# Example: python corpus_reader.py europarl_full_punctuation output_Dataset output.csv da de

#Possible error: when people forget the punctuation, the sentence tokenizer will be messed up

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


#Count the number of occurrences of a symbol in the words
# Re-initialize accumulator
def countExists(numCount, symbol, words):
    if (symbol in words):
        numCount += 1
    return numCount

#Develop the map of existing terms with the # of documents containg it
def uniqueWords(corpusLocationLang):

    domainCorpus = PlaintextCorpusReader(corpusLocationLang, '.*txt')
    distinctListOfWordList = []
    wordFrequencyUpdate = {}

    for i in domainCorpus.fileids():
        distinctWordList = []
        singleTextCorpus = PlaintextCorpusReader(corpusLocationLang, i)
        words = singleTextCorpus.words()
        words = [x.lower() for x in words]

        for w in words:
            if not (w in distinctWordList):
                distinctWordList.append(w)
        distinctListOfWordList.append(distinctWordList)

    for list in distinctListOfWordList:
        for w in list:
            if (w in wordFrequencyUpdate):
                wordFrequencyUpdate[w] += 1
            else:
                wordFrequencyUpdate[w] = 1

    return wordFrequencyUpdate



#Count the number of documents consisting of a specific term
def countDocConsistingTerm(term, corpusLocationLang):
    domainCorpus = PlaintextCorpusReader(corpusLocationLang, '.*txt')
    numDocumentHasWord = 0

    for i in domainCorpus.fileids():
        singleTextCorpus = PlaintextCorpusReader(corpusLocationLang, i)
        words = singleTextCorpus.words()
        words = [x.lower() for x in words]
        
        if (term in words):
            numDocumentHasWord += 1
 
    return numDocumentHasWord

def writeSummary(filename, content, languages):
    contentList = []
    if (os.path.exists(filename)):
        f = open(filename, 'a')
        writer = csv.writer(f)
    else:
        f = open(filename, 'w')
        writer = csv.writer(f)
        writer.writerow(languages)
    if ('euro' in argv[1]):
        contentList.append('EUROPARL')
    elif ('jrc' in argv[1]):
        contentList.append('JRC_ACQUIS')
    else:
        contentList.append('REUTERS')
    for item in content:
        contentList.append(item)
    #contentList.append(content)
    writer.writerow(contentList)


def main():
    listUniCodeChar = u'.!?;'
    languages = [' ']
    numDoc = []
    start_time = time.time()

    for j in range (3, len(argv)):
        corpusLocationLang = os.path.join(os.getcwd(), argv[1], argv[j])
        domainCorpus = PlaintextCorpusReader(corpusLocationLang, '.*txt')

        # CSV detail output
        corpusname = argv[1].split('_')[0]
        print (corpusname)
        outputFile = open(os.path.join(os.getcwd(), argv[2], corpusname + '_' + argv[j] + '.csv'), 'w')
        output_writer = csv.writer(outputFile)
        output_writer.writerow(title)

        totalWords = domainCorpus.words()
        countDocument = 0
        languages.append(argv[j])
        wordFrequencyUpdate = uniqueWords(corpusLocationLang)

        print ("\n")
        print ("Corpus NAME")
        print (argv[1] + ' ' + argv[j])
        print (len(domainCorpus.fileids()))


        for i in domainCorpus.fileids():
            #Initialize empty list for a single file
            distinctWordList = []
            tfidfList = []
            paraLengthList = []
            singleSentDistributionArray = []

            # Re-initialize accumulator
            numNumber = 0
            countDocument += 1
            totalWordLength = 0
            totalSentLength = 0
            numOpenParantheses = 0
            numClosedParantheses = 0
            numHyphen = 0
            numColon = 0
            numForwardSlash = 0
            maxSentLength = 0.0
            numSingleSentPara = 0
            sentLocation = 0

            # Check percentage of completion
            print ("Percentage of completion (in %)")
            print ((countDocument / (float(len(domainCorpus.fileids())))) * 100)

           #Single Document Features
            singleTextCorpus = PlaintextCorpusReader(corpusLocationLang, i)
            words = singleTextCorpus.words()
            words = [x.lower() for x in words]

            sentences = singleTextCorpus.sents()
            paras = singleTextCorpus.paras()
            numWords = len(singleTextCorpus.words())
            numParagraphs = len(paras)
            middleDocument = float (len(sentences)/ 2) #For location calculation later
            wordFreq = {}

            for p in paras:
                sentCount = 0
                #List of words in each paragraph
                for word in p:

                    #Go through each word (punctuation is a word)
                    for w in word:
                        if (w in listUniCodeChar):
                            sentCount +=1
                            sentLocation +=1

                if (sentCount == 1):
                    numSingleSentPara +=1
                    singleSentDistributionArray.append((sentLocation-middleDocument))

                paraLengthList.append(len(p))

            if (len(singleSentDistributionArray) > 0):
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

            for word in words:
                # List of distinct words in the existing document
                if not (word in distinctWordList):
                    distinctWordList.append(word)

                #Frequency of the words in the current document
                if (word in wordFreq):
                    wordFreq[word] +=1
                else:
                    wordFreq [word] = 1

                numOpenParantheses = countExists(numOpenParantheses, '(', word)
                numClosedParantheses = countExists(numClosedParantheses, ')', word)
                numHyphen = countExists(numHyphen, '-', word)
                numForwardSlash = countExists(numForwardSlash,'/', word)
                numColon = countExists(numColon, ':', word)

                if(word.isdigit()):
                    numNumber += 1

                totalWordLength = totalWordLength + len(word)

            # Calculate tf-idf (term frequency - inverse document frequency)
            for wo in wordFreq.keys():
                tf = wordFreq[wo] / len(words)

                if (tf == 0):
                    currenttfidf = 0.0
                else:
                    idf = math.log(len(domainCorpus.fileids()) / wordFrequencyUpdate[wo])
                    currenttfidf = tf * idf

                tfidfList.append(currenttfidf)

            tfidfList.sort(reverse=True)

            averagetfidf = np.mean(tfidfList[0:9])
            typeRatio = len(distinctWordList) / numWords
            paraLengthMean = totalWordLength / numParagraphs

            mapFeatures[i] = [countDocument, numSingleSentPara, ratioSingleSentPara, paraLengthMean,
                              numClosedParantheses,numOpenParantheses, numNumber,
                              numForwardSlash, avgSingleSentDist, numColon, meanSentLength,
                              typeRatio, averagetfidf, numWords, stdParaLength, numHyphen]

            output_writer.writerow([countDocument, i,numSingleSentPara, ratioSingleSentPara, paraLengthMean,
                                    numClosedParantheses, numOpenParantheses, numNumber,
                                    numForwardSlash, avgSingleSentDist, numColon, meanSentLength, typeRatio,
                                    averagetfidf, numWords, stdParaLength, numHyphen])

        print (len(domainCorpus.fileids()))
        numDoc.append(len(domainCorpus.fileids()))

    #writeSummary('Summary.csv', numDoc, languages)
    print ('Elapsed time is', time.time() - start_time)

if __name__ == "__main__":
    main()

