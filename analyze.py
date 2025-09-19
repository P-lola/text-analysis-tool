from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
wordLemmatizer = WordNetLemmatizer()

# Welcome User
def welcomeUser():
    print("Welcome to the text analysis tool. " \
    "\nI will mine and analyze a body of text in a file you give me")

# Get Username
def getUsername():

    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        # Get input from user into the terminal
        inputPrompt = ""
        if attempts == 0:
            inputPrompt = ("To begin, please enter your username:\n")
        else:
            inputPrompt = ("Please, try again:\n")
        usernameFrominput = input(inputPrompt)

        if (len(usernameFrominput) < 4) or (not usernameFrominput.isidentifier()):
            print("Your username must be at least 4 characters long, alphanumeric only,\nhave no spaces, and cannot start with a symbol")
        else:
            return usernameFrominput
        
        attempts += 1

    print("\nExhausted all " + str(maxAttempts) + " attempts, assigning new username...")
    return generate_username()[0]


#Greet the user
def greetUser(name):
    print("Hello " + name + "!")


#Get Text from File
def getArticleText():
    f = open("files/articles.txt", "r")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\r", " ")

#Extract Sentences from Text
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

#Extract Words from text
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

#Get Key sentences based on search pattern of key words
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        #If sentences matches desired pattern, add to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

#Get the average words per sentence excluding punctuation
def getWordPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(" "))
    return totalWords / len(sentences)

#Filter raw tozenized words list to only include
#valid english words 
def cleanseWordList(words):
    cleanseWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for word in words:
        cleanseWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleanseWord)) and len(word) > 1:
            cleanseWords.append(wordLemmatizer.lemmatize(cleanseWord))
    return cleanseWords

# #Get User Details
welcomeUser()
username = getUsername()
greetUser(username)

#Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords= tokenizeWords(articleSentences)

#Get Sentence Analytics
stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordPerSentence(articleSentences)

#Get Word Analytics
aricleWordsCleansed = cleanseWordList(articleWords)

#Print for Test
print("Got:")
print(aricleWordsCleansed)