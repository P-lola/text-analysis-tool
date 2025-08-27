# Welcome User
def welcomeUser():
    print("Welcome to the text analysis tool. " \
    "\nI will mine and analyze a body of text in a file you give me")

# Get Username
def getUsername():
    # Get input from user into the terminal
    usernameFrominput = input("To begin, please enter your username:\n")
    return usernameFrominput

#Greet the user
def greetUser(name):
    print("Hello " + username + "!")


welcomeUser()
username = getUsername()
greetUser(username)
