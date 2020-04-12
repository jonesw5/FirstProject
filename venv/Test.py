# Author: Wesley Jones
# Date: 1/30/2019
# Class: CMSC 416
# Assigment: 'Eliza like'  Program
# Description: Program is to interact with user in away to make the user feel they are speaking with a therapist
import re
import random



# Function takes in a user phrase
# if the phrase has commas, it pulls the last phrase out to analyze only that
# if the phrase is only 1 or 2 words long, proggram reponds with a simple question
# if the hrase is greater than 2 words long, filters are applied to dynamicallly respond to user
# if none of the filters find a specif word or phrase, program simply requests more information
def AnalyzeUserStatement(FullStatement):
    StatementArray = FullStatement.split(", ")
    LastPhrasePos = len(StatementArray)-1

    # Loop through array to find valid statement

    # if StatementArray is only one item long, get out of loop
    CurrentPhrase = StatementArray[LastPhrasePos]
    CurrentStateArray = CurrentPhrase.split()
    skip = True;
    if(len(CurrentStateArray) > 2):
        two_word_phrase = False
    else:
        if (len(CurrentStateArray) < 2):
            noUnderstanding(-1)
            skip = False
        else:
            two_word_phrase = True
    if (skip):
        if(two_word_phrase):
            replace_and_repeat(CurrentPhrase)
        else:
            if (re.compile(r'\bit$').search(CurrentPhrase)):
                TalkBack("Can you describe this \"it\" you speak of?")
            # search for a sense of desire within the user phrase
            # ask why the user wants that
            elif (re.compile(r'\b[Ii] (want|crave|desire|wish|need)\b').search(CurrentPhrase)):
                tokens = re.search('^(.*?)\s(want|crave|desire|wish|need)\s(.*?)$', CurrentPhrase)
                beginning = tokens.group(1)
                middle = tokens.group(2)
                end = tokens.group(3)
                end = end + "?"
                my_string = re.sub('i', "Why do you", beginning) + " " + middle + " " + end
                TalkBack( my_string)
            # search for "I am" within user phrase
            # two potential directions here ( user is sharing a feeling or explaining themselves)
            elif (re.compile(r'\bi am\b').search(CurrentPhrase)):
                tokens = re.search('^(.*?)\sam\s(.*?)$', CurrentPhrase)
                beginning = tokens.group(1)
                end = tokens.group(2)
                end = end + "?"
                temp = isEmotional(end)
                # if emotion is found, program asks specifically about that feeling
                if (temp):
                    my_string = re.sub('i', "What do you think is leading you to feel ", beginning) + temp.group(1)
                # if no emotion is found, simply covert the statement into a qestion
                else:
                    my_string = re.sub('i', "Why are you ", beginning) + end
                TalkBack( my_string)
                isEmotional(end)
            # if a phrase begins possesivesly, repeat the statement as a question changing "my" to "your"
            elif (re.compile(r'^my\b').search(CurrentPhrase)):
                my_string = re.sub(r'^my\b', "Your", CurrentPhrase) + "?"
                my_string = replace_only(my_string)
                TalkBack(my_string)
            # search for the user explicitly sayong "I feel" and ask user to explore thios more
            elif (re.compile(r'\bi feel\b').search(CurrentPhrase)):
                TalkBack(user_name + ", lets explore that feeling a bit deeper")
            # catch potential questions by user and ask the user not to ask questions
            elif (re.compile(r'^(will|what|who|why|when|how)\b').search(CurrentPhrase)):
                TalkBack("Slow down... I am supposed to ask the questions here")
            # if all else fails, go to function for noUnderstanding
            else:
                noUnderstanding(CurrentPhrase)
    return;


# Function to check for specific emotional words within user phrase
# returns the first specific emotional word found
def isEmotional(inputPhrase):
    emotion_list = r'\b(afraid|aggrevated|agressive|agitated|alarmed|amazed|amused|angry|anxious|annoyed|assured|astonished|attracted|bitter|bored|calm|cautious|cheerful|concerned|content|crazy|cruel|delighted|depressed|dissapointed|disgusted|dissatisfied|eager|easy-going|embarressed|envious|excited|facinated|fearful|furious|frustrated|glad|gloomy|greedy|grouchy|guilty|grumpy|happy|hopeless|horrified|homesick|hostile|insecure|insulted|irritated|isolated|jaded|jealous|jittery|jolly|joyful|lazy|loathful|lonely|lustful|mad|merry|mortified|needy|neglected|nervous|optimistic|ornery|outraged|panicked|passionate|pleased|pushy|proud|prideful|pessimistic|relieved|remorseful|resentment|sad|satisified|scared|shocked|shameful|stressed|surprised|sympathetic|spiteful|tense|terrified|thrilled|timid|tormented|uncomfortable|unhappy|upset|vengeful|weary|worried|zestful)\b'
    previous_topic = "what make yous feel " + re.compile(emotion_list).search(inputPhrase).group(1)
    return re.compile(emotion_list).search(inputPhrase)

# function takes in a user phrsde and looks for which person they are speaking in
# is it first, second or third person
# NOTE: not currently used
def whatPerson(inputPhrase):
    person_list = r'\b(my|i|you|he|she)\b'
    per = re.compile(person_list).search(inputPhrase)
    if(per.group(1) == "i"):
        return "you";
    elif (per.group(1) == "my"):
        return "your";
    elif (per.group(1) == "you"):
        return "I";
    elif (per.group(1) == "he"):
        return "he";
    elif (per.group(1) == "she"):
        return "she";
    return "it";

#Function searches through a user phrase for
#   'I' in order to replace with 'you'
#   'you' in order to replace with 'I'
#   'my' in order to replace with 'your'
#  after replacing these items, returns modified phrase to calling function
def replace_only(phrase):
    if (re.compile(r'\byou\b').search(phrase)):
        phrase = re.sub(r'\byou\b', "I", phrase)
    if(re.compile(r'\bi\b').search(phrase)):
        phrase = re.sub(r'\bi\b', "you", phrase)
    if (re.compile(r'\bmy\b').search(phrase)):
        phrase = re.sub(r'\bmy\b', "your", phrase)
    return phrase;

#Function searches through a user phrase for
#   'I' in order to replace with 'you'
#   'you' in order to replace with 'I'
#   'my' in order to replace with 'your'
#  after replacing these items, sned the new phrase to outgoing message
# NOTE: Repeat code here can be consolidated
def replace_and_repeat(phrase):
    if (re.compile(r'\byou\b').search(phrase)):
        phrase = re.sub(r'\byou\b', "I", phrase)
    if(re.compile(r'\bi\b').search(phrase)):
        phrase = re.sub(r'\bi\b', "you", phrase)
    if (re.compile(r'\bmy\b').search(phrase)):
        phrase = re.sub(r'\bmy\b', "your", phrase)

    TalkBack(phrase + " what?")
    return ;

# if the program can't catch a key word or phrase
# a random pregrogrammed response will be given
# a previous topic may potentially be brought back up to steer the conversation
def noUnderstanding(gate):
    if gate != -1:
        gate = random.randint(1, 2)
    else:
        gate = random.randint(0, 2)

    if gate == 0:
        TalkBack("Tell me more")
    if gate == 1:
        TalkBack("I didn't quite understand that, can you rephrase?")
    if gate == 2:
        TalkBack( user_name + ", let's talk about " + previous_topic)

    return ;


# Function takes in a phrase and prepares for output to console
def TalkBack(output):
    print("[Eliza:] " + output)
    return ;


# Begin Main Program
intro = "Hello, I am Eliza, an unlicensed therapist. What is your name?"

user_name = input("[Eliza:] " + intro + "\n[You:] " )


print("[Eliza:] Hello " + user_name + ", What would you like to talk about today?")
KeepGoing = True
previous_topic = "your family"
# Loop Start
# if user types in "bye" or similar request, the loop will be exited
while (KeepGoing):
    userStatement = input( "[" + user_name + ":] " )
    userStatement = userStatement.lower()
    if (re.compile(r'^w[a]+[sz]+[u]+[p]+$').search(userStatement)):
        TalkBack("Waaaazzzzzuuuuppppppp!")
    if (re.compile(r'\b(i want to leave|goodbye|are you a real therapist|how much is this costing me|bye|get me out)\b').search(userStatement)):
        KeepGoing = False
        TalkBack("Ok, we're done here. Goodbye")
    else:
        AnalyzeUserStatement(userStatement)
# Loop End







