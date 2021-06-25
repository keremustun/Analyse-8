# The system is run by running this script
from client import *
from users import *

userTypes = {"1":"Super administrator", "2":"System administrator", "3":"Advisor"}

def login():
    print("Welcome to the CDMS!\n")

    print("Which user type are you?")
    print("Enter 1 to login as a super administrator")
    print("Enter 2 to login as a system administrator")
    print("Enter 3 to login as an advisor")
    userType = input("\nUser type:")
    

    print("\n" + "="*40)
    print("Logged in as: {}".format(userTypes[userType]))

login()
registerUser()

