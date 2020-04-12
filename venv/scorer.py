"""
Author: Wesley Jones
Date: 3/8/2020
Class: CMSC 416
Assignment: 'POS-Scorer'  Program
Description:
             This program takes in a recently tagged file by the tagger.py program and compares
             the resulting tags to a key set. In the end, producing a "confusion matrix" showing
             the accuracy of the tags produced

What's required:
             FileA - this will be the recently tagged data file (FileC in the previous program)
             FileB - this will be the key file containing the expected tags
             FileC - this is the location you would like the information to be outputted to
               without this, the information will be outputted to the terminal, which may be
               difficult to read.

Instructions:
             When calling this program from the command line, you will need to add at least 2 arguements
             command input -->  python tagger.py (FileA) (FileB) > (FileC)
             ex.) "scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt"

             Review the required material above for explanation of arguments

             NOTE: lastly, make sure to separate each argument by a simple space, no comma or punctuation.
              FileC should follow the '>' char

Example:
  >> FileA Contents: (Limited to the first 14 Lines)

        no/DT ,/, it/PRP was/VBD n't/RB
        black/JJ monday/NNP ./. but/CC
        while/IN the/DT new/JJ york/NNP
        stock/NNP exchange/NNP did/VBD
        n't/RB fall/VB apart/NN friday/NNP
        as/IN the/DT dow/NNP jones/NNP
        industrial/NNP average/NNP plunged/VBD
        190.58/NN points/NNS

        ...continues on til end of data


   >> FileB Contents: (Limited to the first 14 Lines)

         No/RB ,/,
        [ it/PRP ]
        [ was/VBD n't/RB Black/NNP Monday/NNP ]
        ./.
        But/CC while/IN
        [ the/DT New/NNP York/NNP Stock/NNP Exchange/NNP ]
        did/VBD n't/RB
        [ fall/VB ]
        apart/RB
        [ Friday/NNP ]
        as/IN
        [ the/DT Dow/NNP Jones/NNP Industrial/NNP Average/NNP ]
        plunged/VBD
        [ 190.58/CD points/NNS ]

        ...continues on til end of data


   >COMMAND PROMPT>
   >>python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt


   >> OUTPUT TO FileC ( pos-tagging-report.txt )

        Accuracy: 83.87%
            PDT	DT	TO	NNS	FW	JJR	(	WDT	)	UH	VBD	:
        PDT	0	0	0	0	0	0	0	0	0	0	0	0
        DT	14	4744	0	0	0	0	0	0	0	1	0	0
        TO	0	0	1243	0	0	0	0	0	0	0	0	0
        NNS	0	0	0	2737	0	0	0	0	0	0	0	0
        FW	0	0	0	0	0	0	0	0	0	0	0	0
        JJR	0	0	0	0	0	152	0	0	0	0	0	0
        (	0	0	0	0	0	0	69	0	0	0	0	0
        WDT	0	0	0	0	0	0	0	136	0	0	0	0
        )	0	0	0	0	0	0	0	0	71	0	0	0
        UH	0	0	0	0	0	0	0	0	0	0	0	0
        VBD	0	0	0	0	0	0	0	0	0	0	1564	0
        :	0	0	0	0	0	0	0	0	0	0	0	334

        ...continues on til end of data
"""

import re
import pandas as pd
# get the user input
import sys

def main():


    # pull the arguments given by the user
    # Example Command as Follows
    # python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
    checkFile = str(sys.argv[1])
    keyFile = str(sys.argv[2])


    compareToData = ReadInFile(checkFile)
    compareToData = RemoveUndesirables(compareToData)
    prefix = "./. "
    compareToData = prefix + compareToData
    compareToArray = ParseToArray(compareToData)


    # keyFile = "pos-test-key.txt"
    keyData = ReadInFile(keyFile)
    keyData = RemoveUndesirables(keyData)
    prefix = "./. "
    keyData = prefix + keyData
    keyArray = ParseToArray(keyData)
    CompareData(compareToArray, keyArray)

    return;





# FUNCTION: ReadInFile
    # read in training file to string variable
def ReadInFile(fil):
    # Read in the file
    with open(fil, 'r', encoding='utf-8') as file:
        fileData = file.read().replace('\n', ' ')
    return fileData;



# FUNCTION: RemoveUndesirables
    # remove phrase boundaried and new lines
def RemoveUndesirables(fileData):
    # fileData = fileData.lower()
    fileData = ' '.join(fileData.split())
    fileData = re.sub('\[ ', '', fileData)
    fileData = re.sub(' ]', '', fileData)
    return fileData;




# FUNCTION: ParseToArray
    # parse the string based on white space
        # the parsed item should be a word/tag tuple
        # will be saved as a string within the array
def ParseToArray(fileData):
    dataArray = fileData.split()
    return dataArray;




# ---------------------------
# Compare to other file
# ---------------------------


def CompareData(testArray, keyArray):

    # grab only tags
    testTags = Tuples2Tags(testArray)
    keyTags = Tuples2Tags(keyArray)


    compareMap = {}
    Tags = set()
    for e in testTags:
        Tags.add(e)
    for e in keyTags:
        Tags.add(e)
    allTags = list(Tags)
    for e in allTags:
        compareMap[e] = [0] * len(allTags)

    for i in range(0, len(testTags)):
        # if testTags[i] != keyTags[i]:
        j = allTags.index(keyTags[i])
        compareMap[testTags[i]][j] += 1

    twoD = []
    for j in compareMap:
        twoD.append(compareMap[j])
    sumCorrect = 0
    sumTotal = 0
    for i in range(0, len(allTags) - 1):
        sumCorrect += twoD[i][i]
        sumTotal += sum(twoD[i])


    accuracy = (sumCorrect / sumTotal) * 100
    print("Accuracy: %4.2f%%"  %(accuracy))


    df = pd.DataFrame.from_dict(twoD)
    df.columns = allTags
    # df = pd.DataFrame.from_dict(compareMap)
    df.index = allTags
    pd.options.display.width = 0
    print(df)

    return ;

def Tuples2Tags(arrayIN):
    arrayOUT = []
    for i in arrayIN:
        mini = i.split("/")
        arrayOUT.append( mini.pop().split('|')[0])
    return arrayOUT;






# ---------------------------
#  Call to Main Program
#   KEEP THIS AT END OF FILE
# ---------------------------
if __name__ == "__main__":
    main()