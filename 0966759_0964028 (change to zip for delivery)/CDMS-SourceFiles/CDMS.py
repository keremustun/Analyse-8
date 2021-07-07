# The system is run by running this script
from users import *
import database

userTypes = {"1":"Advisor", "2":"System administrator", "3":"Super administrator"}
currentUserName = ""

def getLoginType(loggedout):
    print("\n" *40)
    if loggedout:
        print("Logged out...")
    print("="*50)   
    print("Welcome to the CDMS!\n")
    userType = 0
    while userType not in ("1","2","3"):
        
        print("Which user type are you?")
        print("Enter 1 to login as an advisor")
        print("Enter 2 to login as a system administrator")
        print("Enter 3 to login as a super administrator")
        print("Enter 'q' to quit")

        userType = input("\nUser type: ")
        if userType in ("1","2","3"):
            print("\n" *40)
            print("\n" + "="*40)
            print("Login type: {}".format(userTypes[userType]))
            return userType
        elif userType == "q":
            print("\nBye bye!")
            exit()
        else:
            print("\nWrong input")

# Enter username and password
def login(logintypeArg):
    strikes = 0
    loginPassed = False
    while not loginPassed:
        if loginType == '3':
            loginPassed = True
        else:
            print("Enter your username and password")
            username = input("Username: ")
            password = input("Password: ")
            loginPassed = database.AuthenticateLogin(username, password, logintypeArg)

        if loginPassed == "superadmin":
            return "superadmin"
        elif loginPassed == "systemadmin":
            user = database.getUser(username,password,logintypeArg)
            return user
        elif loginPassed == "advisor":
            user = database.getUser(username,password,logintypeArg)
            return user
        else:
            strikes += 1
            if strikes == 5:
                print("You entered a wrong username or password too many times.")
            else:
                print("You entered a wrong username or password. Please try again")


# Login passed, creating user session...
def initializeUser(user,logintypeArg):
    print("\n" * 30)
    getUserName(user)
    if logintypeArg == '1':
        print("Advisor login")
        logAction(username, "Logged In", "Advisor logged in", "No")
        userSession = Advisor(user)
        return userSession

    elif logintypeArg == '2':
        print("System admin login")
        logAction(username, "Logged In", "System Admin logged in", "No")
        userSession = SystemAdmin(user)
        return userSession
        
    else:
        print("Super admin login")
        logAction(username, "Logged In", "Super Admin logged in", "No")
        userSession = SuperAdmin(user)
        return userSession

def showMenu():
    currentUser.showMenu()

def getUserName(user):
    print(user)
    if user == "superadmin":
        currentUserName = "Super Admin"
    else:
        currentUserName = user[0][1]
    

#××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
#×××××××××××××××××××××××××××××××××××××××××××××××× PROGRAM START ×××××××××××××××××××××××××××××××××××××××××××××××××
#××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

running = True
#determining login type
loggedout = False
while running:
    loginType = getLoginType(loggedout)

    #input Username and password
    currentUser = login(loginType)
    currentUser = initializeUser(currentUser,loginType)

    loggedIn = True
    print("\n" * 30)

    while loggedIn:
        loggedIn = showMenu()
        loggedout = True
        


