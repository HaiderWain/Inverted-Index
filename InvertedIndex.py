import glob
import string
from abc import ABC
from html.parser import HTMLParser
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class MyHTMLParser(HTMLParser, ABC):
    temp = ""

    def handle_data(self, data):
        self.temp += data
        return self.temp


# Part 1 - File Reading
path = 'C:/Users/haide/PycharmProjects/InvertedIndexAss1/corpus2/*'
files = glob.glob(path)

# importnat
docindex = 1
wordsList = []
countInTotalCorpus = []
termIdies = 0

DocTermsList = []

# I think these are useless
indexOfWords = []
lastDocumentID = 1
totalDocumentCount = []

# important
docIdsOfEachTerm = []
termIdOfEachTerm = []
stemmedList = []

parser = MyHTMLParser()

for name in files:
    termIdies = 0
    index = 0
    lastDocumentID = docindex
    print(name, docindex)

    eachFile = open(name, encoding='utf-8', errors='ignore')
    contents = eachFile.read()
    eachFile.close()
    # Part 2 - HTML PARSING
    parser.feed(contents)

    # Part 3 - TOKENIZING USING NLTK LIBRARY
    # print(word_tokenize(parser.temp))

    # Part 4 - LOWER CASING TOKENS
    tokenized_text = (word_tokenize(parser.temp.lower()))

    # Part 5 - REMOVING STOP-WORDS
    stopWordFile = open('stoplist.txt', 'r')
    stopWordArray = stopWordFile.read()

    stopWordedArray = [word for word in tokenized_text if word not in stopWordArray]

    # Part 6 - STEMMING THE ARRAY

    stemmer = PorterStemmer()
    for word in stopWordedArray:

        stemmedWord = stemmer.stem(word)

        if len(stemmedWord) == 1:
            continue
        if stemmedWord in string.punctuation:
            continue
        if stemmedWord.isdigit():
            continue
        if stemmedWord[1:].isdigit():
            continue
        if stemmedWord[0] == '-':
            continue

        stemmedList.append(stemmedWord)  # Stores whole dictionary of all files
        # REMOVING CERTAIN GARBAGE CHARACTERS/WORDS
       # stemmedList = [''.join(c for c in s if c not in string.punctuation) for s in stemmedList]
       # stemmedList = [s for s in stemmedList if s]
       # stemmedList = [x for x in stemmedList if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
       # stemmedList = [i for i in stemmedList if len(i) > 1]

        docIdsOfEachTerm.append(docindex)  # Stores docIndex of each word
        termIdOfEachTerm.append(termIdies)  # Stores termIds of each word
        termIdies = termIdies + 1

        # Method-2
        DocTermsList.append([stemmedList.index(stemmedWord), docindex, index])
        index = index + 1

    # Part 7-Writing to files
    newFile10 = open("stemmedList.txt", "a+", encoding='utf-8', errors='ignore')
    for index in range(len(stemmedList)):
        termIDs = newFile10.write(stemmedList[index] + "\n")

    # Part a - Saving document names with their ID's.
    filename = ""
    iterator = 0
    while iterator < len(name):
        if name[iterator] == 'c' and name[iterator + 1] == 'l' and name[iterator + 2] == 'u' and name[
            iterator + 3] == 'e':
            filename = name[iterator:len(name)]
        iterator += 1

    newFile = open("docids.txt", "a+", encoding='utf-8', errors='ignore')
    docIDs = newFile.write(str(docindex) + "\t" + filename + "\n")
    newFile.close()


    # INVERTED INDEX()
    termIndex2 = 0
    newFile3 = open("docANDterms.txt", "a+", encoding='utf-8', errors='ignore')
    for index in range(len(stemmedList)):
        termIDs2 = newFile3.write(str(termIndex2) + "\t" + stemmedList[index] + "\t" + str(docindex) + "\n")
        termIndex2 += 1
    newFile3.close()

    docindex = docindex + 1

# Making of the real inverted index
wordsList = list(dict.fromkeys(stemmedList))

# Part b - Saving tokens with their ID's
termIndex = 0
newFile2 = open("termids.txt", "a+", encoding='utf-8', errors='ignore')
for index in range(len(wordsList)):
    termIDs = newFile2.write(str(termIndex) + "\t" + wordsList[index] + "\n")
    termIndex += 1

newFile2.close()

for k in range(len(wordsList)):
    countInTotalCorpus.append(0)
    totalDocumentCount.append(0)

for i in range(len(wordsList)):
    for j in range(len(stemmedList)):
        if wordsList[i] == stemmedList[j]:
            countInTotalCorpus[i] += 1

name = "docANDterms.txt"
tempFile = open(name, encoding='utf-8', errors='ignore')
contents = tempFile.read()
tempFile.close()

for x in range(len(wordsList)):
    docIndexOnlyForThis = 6000
    for y in range(len(stemmedList)):
        if wordsList[x] == stemmedList[y]:
            if docIdsOfEachTerm[y] == docIndexOnlyForThis:
                doNothing = 0
            else:
                docIndexOnlyForThis = docIdsOfEachTerm[y]
                totalDocumentCount[x] += 1

# Checking outputs
newFile6 = open("docIdsOfEachTerm.txt", "a+", encoding='utf-8', errors='ignore')
for xyz in range(len(docIdsOfEachTerm)):
    newFile6.write(str(docIdsOfEachTerm[xyz]) + "\n")

newFile7 = open("termIdsOfEachTerm.txt", "a+", encoding='utf-8', errors='ignore')
for abc in range(len(termIdOfEachTerm)):
    newFile7.write(str(termIdOfEachTerm[abc]) + "\n")

# The real inverted index
newFile5 = open("finale.txt", "a+", encoding='utf-8', errors='ignore')
for items in range(len(wordsList)):
    newFile5.write(wordsList[items] + "\t" + str(countInTotalCorpus[items]) + "\t" + str(totalDocumentCount[items]) + "\t")

    b = 0
    for a in range(countInTotalCorpus[items]):
        while b < len(stemmedList):
            if wordsList[items] == stemmedList[b]:
                newFile5.write(str(docIdsOfEachTerm[b]) + "," + str(termIdOfEachTerm[b]) + "\t")

            b = b + 1
    newFile5.write("\n")

# The real but not so good inverted index
DocTermsList.sort(key=lambda arr: arr[0])
newFile11 = open("finale2.txt", "a+", encoding='utf-8', errors='ignore')
for rows in range(len(DocTermsList)):
    for columns in range(3):
        newFile11.write(str(DocTermsList[rows][columns]) + "\t")

    newFile11.write("\n")
