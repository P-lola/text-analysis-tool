from random_username.generate import generate_username
import re, nltk, json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('vader_lexicon')
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()

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

#Convert pat of speech from pos_tag function into
#wordnet compatible pos tag
posToWordnetTag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV,
}

def treebankPosTOWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    return wordnet.NOUN

#Convert raw liat of (words, POS) tuple to a list of strings
#that only include valid english words 
def cleanseWordList(posTaggedWordTuples):
    cleanseWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleanseWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleanseWord)) and len(word) > 1 and cleanseWord not in stopWords:
            cleanseWords.append(wordLemmatizer.lemmatize(cleanseWord, treebankPosTOWordnetPos(pos)))
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
wordsPosTagged = nltk.pos_tag(articleWords)
articleWordsCleansed = cleanseWordList(wordsPosTagged)

# Generate word cloud
separator = " "
wordCloudFilePath = "results/wordcloud.png"
wordcloud = WordCloud(width = 1000, height = 700, background_color="white", colormap="tab20b",
                       collocations=False).generate(separator.join(articleWordsCleansed))
wordcloud.to_file(wordCloudFilePath)

#Run Sentiment Analysis
sentimentResult = sentimentAnalyzer.polarity_scores(articleTextRaw)

#Collate analyses into one dictionary
finalResult = {
    "username": username,
    "data": {
        "keySentences": keySentences,
        "wordsPerSentence": round(wordsPerSentence, 1),
        "sentiment": sentimentResult,
        "wordCloudFilePath": wordCloudFilePath
    },
    "metadata": {
        "sentencesAnalyzed": len(articleSentences),
        "wordsAnalyzed": len(articleWordsCleansed)
    }
}
finalResultJson = json.dumps(finalResult, indent=4)

#Print for Test
print(finalResultJson)
