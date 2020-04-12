import re
import re  # importing regular expressions
import random  # importing random numbers
from collections import Counter  # importing counter from collections
from sys import argv

a = 0
b = 0
fNames = []
words = []
dictWords = dict()
dictTags = dict()
tagWord = dict()
tagByPrev = dict()
finala = []


# *tagByPrev[prevTag][tag]/dictTags[prevTag]
# def prob(word, prevTag, tag):
#     temp = ""
#     if temp != prevTag:
#         prob =  ((tagWord[word][tag])/dictWords[word]*tagByPrev[prevTag][tag]/dictTags[prevTag])
#     else:
#         return 0
#     return prob

def tag(data):
    global word
    # finalProb = 0
    prevTag = ''
    for each in data:
        finalProb = 0
        word = each
        finalTag = ""
        currProb = 0
        if each not in dictWords:
            myTag = "NN"
        else:
            keys = tagWord[word].keys()
            for key in keys:
                # print(key)
                if key != '':
                    a = tagWord[each][key]
                    b = dictWords[each]
                    if key not in tagByPrev[prevTag]:
                        c = 0
                        d = 1
                    else:
                        c = tagByPrev[prevTag][key]
                        d = dictTags[prevTag]
                    currProb = (a / b) * (c / d)
                    print( "a =" + str(a) + "\tb =" + str(b) + "\tc =" + str(c) + "\td =" + str(d) + "\tkey =" + key  + "\tprob1 =" + str(currProb)  + "\tprob2 =" + str(finalProb)  )
                    if finalProb < currProb:
                        print("Made it In")
                        finalProb = currProb;
                        finalTag = key
                prevTag = key
            print(finalTag)
            print(each + '/' + finalTag)


def main():
    trainFile = "pos-train.txt"
    testFile = "pos-test.txt"

    File = open(trainFile, 'r', encoding='utf-8')
    contents = File.read()
    contents = re.sub(r'\[', '', contents)
    contents = re.sub(r'\[ ', '', contents)
    contents = re.sub(r' \]', '', contents)
    contents = re.split(r'\s+', contents)
    prevWord = ''
    prevTag = ''
    for element in contents:
        wTag = re.split('/', element)
        passed = 2
        currLen = len(wTag)
        if currLen < passed:
            continue
        currWord = wTag[0]
        currTag = wTag[1]

        if currWord not in dictWords.keys():
            dictWords[currWord] = 1
        else:
            dictWords[currWord] = dictWords[currWord] + 1

        if currTag not in dictTags.keys():
            dictTags[currTag] = 1
        else:
            dictTags[currTag] = dictTags[currTag] + 1

        if currWord in tagWord.keys():
            if currTag in tagWord[currWord].keys():
                tagWord[currWord][currTag] = tagWord[currWord][currTag] + 1
            else:
                tagWord[currWord][currTag] = 1
        else:
            tagWord[currWord] = {}
            tagWord[currWord][currTag] = 1

        if prevTag in tagByPrev.keys():
            if currTag in tagByPrev[prevTag].keys():
                tagByPrev[prevTag][currTag] = tagByPrev[prevTag][currTag] + 1
            else:
                tagByPrev[prevTag][currTag] = 1
        else:
            tagByPrev[prevTag] = {}
            tagByPrev[prevTag][currTag] = 1
        currWord = prevWord
        prevTag = currTag

    File.close()

    File1 = open(testFile, 'r', encoding='utf-8')
    cont = File1.read()
    cont = re.sub(r'\[ ', '', cont)
    cont = re.sub(r' \]', '', cont)
    cont = re.split(r'\s+', cont)
    tag(cont)
    print(dictTags)
    print(dictWords)
    print(tagByPrev)
    print(tagWord)


main()
