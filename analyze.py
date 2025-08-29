from random_username.generate import generate_username

# Welcome User
def welcomeUser():
    print("Welcome to the text analysis tool. " \
    "\nI will mine and analyze a body of text in a file you give me")

# Get Username
def getUsername():
    # Get input from user into the terminal
    usernameFrominput = input("To begin, please enter your username:\n")

    if (len(usernameFrominput) < 4) or (not usernameFrominput.isidentifier()):
        print("Your username must be at least 4 characters long, alphanumeric only,\nhave no spaces, and cannot start with a symbol")
        usernameFrominput = generate_username()[0]
        print(usernameFrominput)
        print("Assigning new username...")

    return usernameFrominput

#Greet the user
def greetUser(name):
    print("Hello " + name + "!")


welcomeUser()
username = getUsername()
greetUser(username)
