# The system is run by running this script
from users import *
from database import AuthenticateLogin, getUser
import currentuser

userTypes = {"1":"Advisor", "2":"System administrator", "3":"Super administrator"}

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
    global currentUserName
    strikes = 0
    loginPassed = False
    while not loginPassed:
        # if loginType == '3':
        #     loginPassed = True
        # else:
            print("\nEnter your username and password")
            username = input("Username: ")
            password = input("Password: ")
            loginPassed = AuthenticateLogin(username, password, logintypeArg)

            if loginPassed == "superadmin":
                currentuser.currentUserName = "superadmin"
                return 
            elif loginPassed == "systemadmin":
                currentuser.currentUserName = username
                return 
            elif loginPassed == "advisor":
                currentuser.currentUserName = username
                return 
            else:
                strikes += 1
                if strikes % 5 == 0:
                    username = ""
                    print("\nYou entered a wrong username or password too many times. Action logged as suspicious.")
                    logAction("User tries to log in", f"Login failed too many times, Username used: {username}, Password used: {password}", "Yes")
                    import time
                    blocktime =  (strikes * 6) 
                    while blocktime > 0:
                        if blocktime != 1:
                            print(f"You can log in after {blocktime} seconds")
                        else:
                            print(f"You can log in after {blocktime} second")

                        blocktime -= 1
                        time.sleep(1)
                    
                    

                else:
                    print("You entered a wrong username or password. Please try again")
                    logAction("User tries to log in", f"Login failed, Username used: {username}, Password used: {password}", "No")


# Login passed, creating user session...
def initializeUser(logintypeArg):
    print("\n" * 30)
    userSession = ""
    if logintypeArg == '1':
        userSession = Advisor()
        logAction("Logged In", "Advisor logged in", "No")

    elif logintypeArg == '2':
        userSession = SystemAdmin()
        logAction("Logged In", "System Admin logged in", "No")
        
    else:
        userSession = SuperAdmin()
        logAction("Logged In", "Super Admin logged in", "No")

    return userSession

def showMenu():
    currentUser.showMenu()

    

#××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
#×××××××××××××××××××××××××××××××××××××××××××××××× PROGRAM START ×××××××××××××××××××××××××××××××××××××××××××××××××
#××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

running = True
#determining login type
loggedout = False
while running:
    print (ord("1"))
    loginType = getLoginType(loggedout)

    #input Username and password
    currentUser = login(loginType)
    currentUser = initializeUser(loginType)

    loggedIn = True
    print("\n" * 30)

    while loggedIn:
        loggedIn = showMenu()
        loggedout = True
        

# def validateInput(input):

