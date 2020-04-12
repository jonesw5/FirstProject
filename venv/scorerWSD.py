"""
Author: Wesley Jones
Date: 3/31/2020
Class: CMSC 416
Assignment: 'WSD-Scorer'  Program
Description:
             This program takes in a recently line sense tagged file by the wsd.py program and compares
             the resulting sense ID's to a key set. In the end, producing a "confusion matrix" showing
             the accuracy of the sense ID's produced

What's required:
             FileA - this will be the recently ID'd data file (FileC in the previous program)
             FileB - this will be the key file containing the expected ID's
             FileC - this is the location you would like the information to be outputted to
               without this, the information will be outputted to the terminal, which may be
               difficult to read.

Instructions:
             When calling this program from the command line, you will need to add at least 2 arguments
             command input -->  python scorer.py (FileA) (FileB) > (FileC)
             ex.) "scorer.py my-line-answers.txt line-key.tx > pos-tagging-report.txt"

             Review the required material above for explanation of arguments

             NOTE: lastly, make sure to separate each argument by a simple space, no comma or punctuation.
              FileC should follow the '>' char

Example:
  >> FileA Contents: (Limited to the first 6 Lines)

        <answer instance="line-n.w8_059:8174:" senseid="phone"/>
        <answer instance="line-n.w7_098:12684:" senseid="phone"/>
        <answer instance="line-n.w8_106:13309:" senseid="phone"/>
        <answer instance="line-n.w9_40:10187:" senseid="phone"/>
        <answer instance="line-n.w9_16:217:" senseid="phone"/>
        <answer instance="line-n.w8_119:16927:" senseid="product"/>

        ...continues on til end of data


   >> FileB Contents: (Limited to the first 6 Lines)

        <answer instance="line-n.w8_059:8174:" senseid="phone"/>
        <answer instance="line-n.w7_098:12684:" senseid="phone"/>
        <answer instance="line-n.w8_106:13309:" senseid="phone"/>
        <answer instance="line-n.w9_40:10187:" senseid="phone"/>
        <answer instance="line-n.w9_16:217:" senseid="phone"/>
        <answer instance="line-n.w8_119:16927:" senseid="product"/>

        ...continues on til end of data


   >COMMAND PROMPT>
   >>python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt


   >> OUTPUT TO FileC ( pos-tagging-report.txt )

        Accuracy: 100.0%
                phone product
        phone	387		0
        product	 0		239

        ...continues on til end of data
"""

import re
import pandas as pd
# get the user input
import sys
senseID_list = []
def main():


    # pull the arguments given by the user
    # Example Command as Follows
    # python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
    checkFile = str(sys.argv[1])
    keyFile = str(sys.argv[2])

    global senseID_list
    senseID_list = []

    test_data = ReadInFile(checkFile)
    BreakupFile(test_data)
    testSenseID_list = senseID_list

    key_data = ReadInFile(keyFile)
    BreakupFile(key_data)
    keySenseID_list = senseID_list

    totalCount = len(keySenseID_list)
    correct = 0
    matr = [[0, 0], [0, 0]]
    for i in range(0, len(keySenseID_list)):
        if testSenseID_list[i] == keySenseID_list[i]:
            correct += 1
            if 'phone' in testSenseID_list[i]:
                matr[0][0] += 1
            else:
                matr[1][1] += 1
        else:
            if 'phone' in testSenseID_list[i]:
                matr[0][1] += 1
            else:
                matr[1][0] += 1

    result = correct / totalCount * 100

    print("Accuracy: " + str(result) + "%")
    print("\t\tphone product")
    print("phone\t" + str(matr[0][0]) + "\t\t" + str(matr[0][1]))
    print("product\t " + str(matr[1][0]) + "\t\t" + str(matr[1][1]))


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
    return fileData;

k = 7

def BreakupFile(fileData):
    fileData = fileData.split('\n')
    isReady = False
    for line in fileData:
        senseID = ""
        if "<answer " in line:
            # find senseID
            senseID = line[ : -3: ]
            senseID = senseID[senseID.index("senseid=") + 9 : : ]
            senseID_list.append(senseID)
    return ;



# ---------------------------
#  Call to Main Program
#   KEEP THIS AT END OF FILE
# ---------------------------
if __name__ == "__main__":
    main()