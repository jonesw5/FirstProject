"""
Author: Wesley Jones
Date: 3/31/2020
Class: CMSC 416
Assignment: 'Sentiment Analysis'  Program
Description:
             METHOD USED: DECISION LIST
             This program takes in pre-"Sentiment Analysized" data to train itself on "tagging" sentences
             by it context and then applies itself to another untagged data file. Outputting a copy of the
             second file with newly associated context tags

What's required:
             FileA - this will be your training data. The words and punctuation found within this file
              should be manually preTagged
             FileB - this will be the file that you want to apply your newly trained WSD program to.
               The word and punctuation found within in this file need to be without tags
             FileC - this is the location you would like the information to be outputted to
               without this, the information will be outputted to the terminal, which may be
               difficult to read.

Instructions:
             When calling this program from the command line, you will need to add at least 2 arguments
             command input -->  python wsd.py (FileA) (FileB) > (FileC)
             ex.) "python wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt"

             Review the required material above for explanation of arguments

             NOTE: lastly, make sure to separate each argument by a simple space, no comma or punctuation.
              FileC should follow the '>' char

Example:
  >> FileA Contents: (Limited to the first 2 Linestags)

        <corpus lang="en">
        <lexelt item="sentiment">
        <instance id="620821002390339585">
        <answer instance="620821002390339585" sentiment="negative"/>
        <context>
        Does @macleansmag still believe that Ms. Angela Merkel is the "real leader of the free world"?  http://t.co/isQfoIcod0 (Greeks may disagree
        </context>
        </instance>
        <instance id="621090050848198657">
        <answer instance="621090050848198657" sentiment="negative"/>
        <context>
        By Michael Nienaber BERLIN, July 10 (Reuters) - The parties in Angela Merkel's coalition government sent conflicting signals on the latest
        </context>

        (...continues on til end of data ending with)
        </lexelt>
        </corpus>


   >> FileB Contents: (Limited to the first 14 Lines)

        <corpus lang="en">
        <lexelt item="sentiment">
        <instance id="620979391984566272">
        <context>
        On another note, it seems Greek PM Tsipras married Angela Merkel to Francois Hollande on Sunday #happilyeverafter http://t.co/gTKDxivf79
        </context>
        </instance>
        <instance id="621340584804888578">
        <context>
        Amazon Prime Day is just like Black Friday if you only buy bulk protein powder and will-making software on Black Friday.
        </context>

        (...continues on til end of data ending with)
        </lexelt>
        </corpus>

   >COMMAND PROMPT>
   >> python sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-line-answers.txt


   >> OUTPUT TO FileC ( pos-test-with-tags.txt )

        #<answer instance="620821002390339585">:" senseid="negative"/>
        #<answer instance="621090050848198657">:" senseid="positive"/>

        ...continues on til end of data

"""

import re
# get the user input
import sys
import numpy as math


# ---------------------------
# Main Program Starts Here
# ---------------------------


testFile = ""
trainFile = ""
senseID_list = []
context_list = []
lineID_list = []
uniqueIDs = []
totalWords = 0
outputFile = ""

def main():


    # DataStructures
    global FT_F_Sense
    global senseID_list
    global context_list
    FT_F_Sense = {0 :{}}  # [Type] _ [Feature] _ [Sense] _ count
    # == MAP<> Key-> 'word' | Value -> (MAP<> Key-> 'tag' | value -> count)
    # global Sense2Word
    # Tag2TagMap = {"" :{}} # == MAP<> Key-> 'tag(i-1)' | Value - (MAP<> Key-> 'tag(i)' | value -> count)
    # global Tag2WordMap

    GrabCommandLineInput()
    # HardCodeFileNames()

    trainingData = ReadInFile(trainFile)
    BreakupFile(trainingData)
    buildDictionary()
    # rankThem()
    # apply to test
    senseID_list.clear()
    context_list.clear()
    testingData = ReadInFile(testFile)
    BreakupFile(testingData)
    makeSense()
    # scorer()





# FUNCTION: GrabCommandLineInput
def GrabCommandLineInput():
    global  trainFile
    global  testFile
    # pull the arguments given by the user
    # Example Command as Follows
    # python wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt
    trainFile = str(sys.argv[1])
    testFile = str(sys.argv[2])
    return;

# FUNCTION: GrabCommandLineInput
def HardCodeFileNames():
    # For Testing only
    global trainFile
    trainFile = "sentiment-train.txt"
    global testFile
    testFile = "sentiment-test.txt"
    return;


# FUNCTION: ReadInFile
    # read in training file to string variable
def ReadInFile(fil):
    # Read in the file
    with open(fil, 'r', encoding='utf-8') as file:
        fileData = file.read()
    return fileData;


# FUNCTION: RemoveUndesirables
    # remove phrase boundaried and new lines
def RemoveUndesirables(fileData):
    fileData = fileData.lower()
    fileData = ' '.join(fileData.split())
    fileData = re.sub('<s>', '', fileData)
    fileData = re.sub('<p>', '', fileData)
    fileData = re.sub('<@>', '', fileData)
    fileData = re.sub('</p>', '', fileData)
    fileData = re.sub('</s>', '', fileData)
    fileData = re.sub('[?.,\'\"]', '', fileData)
    return fileData;

k = 7

def BreakupFile(fileData):
    fileData = fileData.split('\n')
    isReady = False
    for line in fileData:
        senseID = ""
        context = ""
        if "<answer " in line:
            # find senseID
            senseID = line[ : -3: ]
            senseID = senseID[senseID.index("sentiment=") + 11 : : ]
            senseID_list.append(senseID)
        elif isReady :
            # add line to context array
            context = RemoveUndesirables(line)
            context_list.append(context)
            isReady = False
        elif "<context>" in line:
            # prepare for context input
            isReady = True
        elif "</context>" in line:
            # closed for context input
            isReady = False
        elif "<instance id=" in line:
            lineID = re.sub('<instance id="', '', line)
            lineID = re.sub(':">', '', lineID)
            lineID_list.append(lineID)
    return ;

def buildDictionary():
    global  uniqueIDs
    uniqueIDs = set(senseID_list)
    uniqueIDs = list(uniqueIDs)


    # loop thru context list and grab features
    # find feature index
    indexC = 0
    for cont in context_list:
        con = cont.split()
        for word in con:
            addToList(0, word, senseID_list[indexC])
        indexC += 1


    return ;


def makeSense():
    global FT_F_Sense
    global senseID_list
    # loop thru context list and grab features
    # find feature word
    indexC = 0
    runningCount = [0,0]
    for cont in context_list:
        con = cont.split()
        runningScore = [0,0]
        for word in con:
            if FT_F_Sense[0].get(word, -1) != -1 :
                # which count is higher?
                if FT_F_Sense[0][word].get(uniqueIDs[0]) > FT_F_Sense[0][word].get(uniqueIDs[1]):
                    runningScore[0] += FT_F_Sense[0][word].get('log')
                else:
                    runningScore[1] += FT_F_Sense[0][word].get('log')

        sense = ""

        if senseID_list.count(uniqueIDs[0]) > senseID_list.count(uniqueIDs[1]):
            sense = uniqueIDs[0]
        else:
            sense = uniqueIDs[1]

        if runningScore[0] > runningScore[1]:
            sense = uniqueIDs[0]
            runningCount[0] += 1
        elif runningScore[0] < runningScore[1]:
            sense = uniqueIDs[1]
            runningCount[1] += 1

        # print(sense)
        #<answer instance="line-n.w8_008:13756:" senseid="phone"/>
        stringOut = "#<answer instance=\"" + lineID_list[indexC] + ":\" sentiment=\"" + sense + "\"/>"
        # outputFile += stringOut + "\n"
        print(stringOut)
        senseID_list.append(sense)
        indexC += 1

    # print(runningCount)
    return ;



# dict(word, (key : count)


def addToList(firstKey, secondKey, thirdKey):
    global totalWords
    global senseID_list
    global uniqueIDs
    totalWords += 1
    global FT_F_Sense
    if FT_F_Sense.get(firstKey, -1) == -1 :
        FT_F_Sense[firstKey] = {secondKey: {uniqueIDs[0]: 0}}
        FT_F_Sense[firstKey][secondKey][uniqueIDs[1]] = 0
    elif FT_F_Sense[firstKey].get(secondKey, -1) == -1:
        FT_F_Sense[firstKey][secondKey] = {uniqueIDs[0]: 0}
        FT_F_Sense[firstKey][secondKey][uniqueIDs[1]] = 0


    FT_F_Sense[firstKey][secondKey][thirdKey] += 1


    string = "log"
    if senseID_list.count(uniqueIDs[0]) > 0:
        val_1 = FT_F_Sense[firstKey][secondKey].get(uniqueIDs[0], 0) / senseID_list.count(uniqueIDs[0])
    else:
        infiniteNom = True
    if senseID_list.count(uniqueIDs[1]) > 0:
        val_2 = FT_F_Sense[firstKey][secondKey].get(uniqueIDs[1], 0) / senseID_list.count(uniqueIDs[1])
    else:
        infiniteDenom = True

    infiniteDenom = False
    infiniteNom = False
    # |log( (word | sense1) / (word | sense2) ) |
    if (val_1 == 0 or infiniteDenom):
        result = 1
    elif val_2 == 0 or infiniteNom:
        result = 0
    else:
        result = math.log10(val_1 / val_2)
    # print(val_1,val_2)
    if result < 0:
        result = result * -1
    FT_F_Sense[firstKey][secondKey][string] = result

    return True;





def scorer():
    global  senseID_list
    # senseID_list = []
    BreakupFile(outputFile)
    testSenseID_list = senseID_list

    senseID_list.clear()
    keyfile = "sentiment-test-key.txt"
    key_data = ReadInFile(keyfile)
    BreakupFile(key_data)
    keySenseID_list = senseID_list

    print("total key count  = " + str(len(keySenseID_list)))
    print("total test count = " + str(len(testSenseID_list)))
    totalCount = len(keySenseID_list)
    correct = 0
    matr = [[0, 0], [0, 0]]
    for i in range(0, len(keySenseID_list)):
        if testSenseID_list[i] == keySenseID_list[i]:
            correct += 1
            if uniqueIDs[0] in testSenseID_list[i]:
                matr[0][0] += 1
            else:
                matr[1][1] += 1
        else:
            if uniqueIDs[0] in testSenseID_list[i]:
                matr[0][1] += 1
            else:
                matr[1][0] += 1

    result = correct / totalCount * 100

    print("Accuracy: " + str(result) + "%")
    print("\t\t" + uniqueIDs[0] + " " + uniqueIDs[1])
    print(uniqueIDs[0] + "\t" + str(matr[0][0]) + "\t\t" + str(matr[0][1]))
    print(uniqueIDs[1] + "\t " + str(matr[1][0]) + "\t\t" + str(matr[1][1]))
    return ;







# ---------------------------
#  Call to Main Program
#   KEEP THIS AT END OF FILE
# ---------------------------
if __name__ == "__main__":
    main()