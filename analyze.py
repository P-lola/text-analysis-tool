from random_username.generate import generate_username

from nltk.tokenize import word_tokenize, sent_tokenize

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
def tokenizeWords(sentences);
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words



#Get User Details
welcomeUser()
username = getUsername()
greetUser(username)

#Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWorks= tokenizeWords(articleSentences)

#Print for Test
print("Got:")
for sentenceTest in articleSentences:
    print(sentenceTest + "\n")