"""
Author: Wesley Jones
Date: 3/8/2020
Class: CMSC 416
Assignment: 'POS-Tagger'  Program
Description:
             This program takes in pre-"tagged" data to train itself on "tagging" words and then applies
              itself to another untagged data file. Outputting a copy of the second file with newly
              associated tags

What's required:
             FileA - this will be your traning data. The words and punctuation found within this file
              should be manually preTagged
             FileB - this will be the file that you want to apply your newly trained POS-Tagger to.
               The word and punctuation found within in this file need to be without tags
             FileC - this is the location you would like the information to be outputted to
               without this, the information will be outputted to the terminal, which may be
               difficult to read.

Instructions:
             When calling this program from the command line, you will need to add at least 2 arguements
             command input -->  python tagger.py (FileA) (FileB) > (FileC)
             ex.) "python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt"

             Review the required material above for explanation of arguments

             NOTE: lastly, make sure to separate each argument by a simple space, no comma or punctuation.
              FileC should follow the '>' char

Example:
  >> FileA Contents: (Limited to the first 14 Lines)

        [ Pierre/NNP Vinken/NNP ]
        ,/,
        [ 61/CD years/NNS ]
        old/JJ ,/, will/MD join/VB
        [ the/DT board/NN ]
        as/IN
        [ a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ]
         ./.
         [ Mr./NNP Vinken/NNP ]
         is/VBZ
         [ chairman/NN ]
         of/IN
         [ Elsevier/NNP N.V./NNP ]
         ,/,

        ...continues on til end of data


   >> FileB Contents: (Limited to the first 14 Lines)

         No ,
         [ it ]
         [ was n't Black Monday ]
         .
         But while
         [ the New York Stock Exchange ]
         did n't
         [ fall ]
         apart
         [ Friday ]
         as
         [ the Dow Jones Industrial Average ]
         plunged
         [ 190.58 points ]

        ...continues on til end of data

   >COMMAND PROMPT>
   >> python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt


   >> OUTPUT TO FileC ( pos-test-with-tags.txt )

        no/DT ,/, it/PRP was/VBD n't/RB
        black/JJ monday/NNP ./. but/CC
        while/IN the/DT new/JJ york/NNP
        stock/NNP exchange/NNP did/VBD
        n't/RB fall/VB apart/NN friday/NNP
        as/IN the/DT dow/NNP jones/NNP
        industrial/NNP average/NNP plunged/VBD
        190.58/NN points/NNS

        ...continues on til end of data
"""
import re
import pandas as pd
# get the user input
import sys

# ---------------------------
# Main Program Starts Here
# ---------------------------

def main():
    # global outputFile

    # DataStructures
    global Word2TagMap
    Word2TagMap = {"" :{}} # == MAP<> Key-> 'word' | Value -> (MAP<> Key-> 'tag' | value -> count)
    global Tag2TagMap
    Tag2TagMap = {"" :{}} # == MAP<> Key-> 'tag(i-1)' | Value - (MAP<> Key-> 'tag(i)' | value -> count)
    global Tag2WordMap
    Tag2WordMap= {"" :{}} # == MAP<> Key-> 'tag' | Value -> (MAP<> Key-> 'word' | value -> count)


    # pull the arguments given by the user
    # Example Command as Follows
    # python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
    trainFile = str(sys.argv[1])
    tagThisFile = str(sys.argv[2])

    # trainFile = "pos-train.txt"
    # tagThisFile = "pos-test.txt"
    trainingData = ReadInFile(trainFile)
    trainingData = RemoveUndesirables(trainingData)
    prefix = "./. "
    trainingData = prefix + trainingData
    trainArray = ParseToArray(trainingData)
    BuildTheMaps(trainArray)

    exploreData = ReadInFile(tagThisFile)
    exploreData = RemoveUndesirables(exploreData)
    # prefix = ". "
    # exploreData = prefix + exploreData
    exploreArray = ParseToArray(exploreData)
    # should be an array of just words and punction
    taggedData = TagTheData(exploreArray)

    outputData = Data2String(taggedData)
    PrintDataOut(outputData)
    return




# FUNCTION: GrabCommandLineInput
def GrabCommandLineInput():
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

#FUNCTION: BuildTheMaps
    # Loop through array
        # update Word2TagMap
        # update Tag2TagMap
        # update Tag2WordMap
def BuildTheMaps(inputData):
    prev_Tag = "."
    for i in range(0, len(inputData)):
        wordTagTuple = AnalyzeTuple(inputData[i])
        cur_Tag = wordTagTuple[0].split('|')[0]
        for j in range(1, len(wordTagTuple)):
            cur_word = wordTagTuple[j].lower()
            Update_Word2TagMap(cur_word, cur_Tag, prev_Tag)
            Update_Tag2TagMap(cur_word, cur_Tag, prev_Tag)
            Update_Tag2WordMap(cur_word, cur_Tag, prev_Tag)
        prev_Tag = cur_Tag
    return ;


"""
def BuildTheMaps(inputData):
    prev_Tag = "."
    for i in range(0, len(inputData)):
        wordTagTuple = AnalyzeTuple(inputData[i])
        cur_Tag = wordTagTuple[0].split('|')[0]
        for j in range(1, len(wordTagTuple)):
            cur_word = wordTagTuple[j].lower()
            Update_Word2TagMap(cur_word, cur_Tag, prev_Tag)
            Update_Tag2TagMap(cur_word, cur_Tag, prev_Tag)
            Update_Tag2WordMap(cur_word, cur_Tag, prev_Tag)
        prev_Tag = cur_Tag
    return ;
    
    Function BuildYourDictionaries(String[] dataArray)
        previousTag = "."
        For each (element in dataArray)
            // should expect element to equal "SomeWord/SomeTag"
            // if you 
            miniArray = element.split("/")
            word = miniArray[0]
            tag = miniArray.reverse()[0]
            
            // add elements to your dictionary of words
            dictionaryWords[word] = {tag : 1} // the '1' is the count
            if already exists, up the count by one
            
            // add tag to dictionary of tags
            dictionaryTags[previousTag] = {currentTag : 1} // '1' being the count
            if already exists, up the count
            
            previousTag = currentTag
            

Function TagYourData (String[] dataArray)
            previousTag = "."
            For each (element in dataArray)
            // should expect element to equal "SomeWordHere"
            word = element.split("/")[0]
            
            // Does the word exist in the dictionary?
            if dictionaryWord.get(word, -1) == -1: // if the result is -1, its not found
                myTag = "NN"
            else:
                // P(tag|word)*P(tag|previous tag)
                // find P(tag(i)/word(i)), if either is zero, force all zero
                // find P(tag(i)/tag(i-1)), if either is zero, force all zero
                // multiply both to get the probability
                // NOTE: You will have to iterate thru all possible tags 
                //      allPossibleTags = dictionaryWords[word].keys() 
                //      this will give a list to iterate thru
                //      Keep track of the highest probable tag and it probabilty
                        if currentProbability > newHighestProbability
                            newHighestProbability = currentProbability
                            newHighestProbableTag = currentTag_with_currentProbabilty
                Will_Use_This_Tag = newHighestProbableTag
                
                dataArray[index] = element + "/" + Will_Use_This_Tag
            
            (And you can figure how to print it out)
            
            
            
            
            
    For the scorer.py
        Just read in both files as string arrays
        String[] fileData1 = []
        String[] fileData2 = []
        // find a way to get all potential tags into an array
        String[] all_possible_tags = []
        
        for i=0, i < fileData.length i++
            String a = fileData1[i].split("/").reverse()[0]           
            String b = fileData2[i].split("/").reverse()[0]
            
            // find index of a & b in all_possible_tags
            row = all_possible_tags.index(a)
            col = all_possible_tags.index(b)
            
            Build a 2D array of the counts
            counts[row][col] ++
            
    
    * Then print the 2D array using the all_possible_tags as header and row index
            
            
            
            
            
            
"""





# FUNCTION: Update_Word2TagMap
def Update_Word2TagMap(cur_word, cur_Tag, prev_Tag):
    if Word2TagMap.get(cur_word, -1) == -1:
        val = {cur_Tag : 1}
        Word2TagMap[cur_word] = val
    else:
        if Word2TagMap[cur_word].get(cur_Tag, -1) == -1:
            Word2TagMap[cur_word][cur_Tag] = 1
        else:
            Word2TagMap[cur_word][cur_Tag] += 1
    return ;

def Update_Tag2TagMap(cur_word, cur_Tag, prev_Tag):
    if Tag2TagMap.get(prev_Tag, -1) == -1:
        val = {cur_Tag : 1}
        Tag2TagMap[prev_Tag] = val
    else:
        if Tag2TagMap[prev_Tag].get(cur_Tag, -1) == -1:
            Tag2TagMap[prev_Tag][cur_Tag] = 1
        else:
            Tag2TagMap[prev_Tag][cur_Tag] += 1
    return ;

def Update_Tag2WordMap(cur_word, cur_Tag, prev_Tag):
    if Tag2WordMap.get(cur_Tag, -1) == -1:
        val = {cur_word : 1}
        Tag2WordMap[cur_Tag] = val
    else:
        if Tag2WordMap[cur_Tag].get(cur_word, -1) == -1:
            Tag2WordMap[cur_Tag][cur_word] = 1
        else:
            Tag2WordMap[cur_Tag][cur_word] += 1
    return ;

# FUNCTION: Update_Tag2TagMap
# FUNCTION: Update_Tag2WordMap

#FUNCTION: AnalyzeTuple
    # Does the tuple conform to the expected layout
def AnalyzeTuple(inputTuple):
    # does a '\/' exist?
        #if so how many?
    oldArray = inputTuple.split("\/")
    newArray = []
    for i in oldArray:
        newArray += i.split('/')
    #reverse array
    newArray.reverse()
    newArray[0] = newArray[0].split('|')[0]
    return newArray; # Return an Array ['tag', 'word', 'word',...etc]




def TagTheData(wordArray):
    # Take in Array of words and punctuation
    # Loop through and tag each word/punctuation with proper tag

    prev_word = "."
    prev_Tag = "."
    prev_TagMap = Tag2TagMap[prev_Tag]
    # exit()
    for i in range(0, len(wordArray) - 1):
        cur_Word = wordArray[i].lower()
        cur_Word = cur_Word.split("/")[0]
        topProb = 0
        topTag = "NN"
        # P(tag|word)*P(tag|previous tag)
        #        a   x   b
        if Word2TagMap.get(cur_Word, -1) == -1:
            givenTag = "NN"
        else:
            # loop through tags associated with word
            #  calc the greatest prob out of all
            prev_TagMap = {}
            prev_TagMap = Tag2TagMap[prev_Tag]
            sumTotal_PrevTag = sum(prev_TagMap.values())
            for j in Word2TagMap[cur_Word].keys():
                # j is a potential tag
                if sumTotal_PrevTag != 0:
                    part_b = (prev_TagMap.get(j, 0) / sumTotal_PrevTag)
                else:
                    part_b = 0
                part_a = Word2TagMap[cur_Word].get(j,0) / sum(Word2TagMap[cur_Word].values())
                if topProb < (part_a * part_b):
                    topProb = (part_a * part_b)
                    topTag = j
                # end if
            #end for j
            givenTag = topTag
        # end if/else
        wordArray[i] = cur_Word + "/" + givenTag
        prev_Tag = givenTag
    # end for i
    return wordArray;


def PrintDataOut(outputDataArray):
    print(outputDataArray)

    return ;


def Data2String(dataArray):
    j = 0
    output = ""
    for i in dataArray:
        j = j + len(i)
        i += " "
        if j > 25:
            i += "\n"
            j = 0
        output += i
    return output;



# ---------------------------
#  Call to Main Program
#   KEEP THIS AT END OF FILE
# ---------------------------
if __name__ == "__main__":
    main()