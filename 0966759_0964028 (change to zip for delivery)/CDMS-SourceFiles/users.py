from client import registerClient

def registerUser():
    registerType = ""
    while registerType == "":
        print("\nWhat type of user do you want to register?")
        print("Enter 1 to register a system administrator")
        print("Enter 2 to register an advisor")
        print("Enter 3 to register a client")
        print("Enter 'x' to go back")
        registerType = input("Register type: ")
        
        if(registerType == "1"):
            registerSystemAdmin()
        elif (registerType == "2"):
            registerAdvisor()
        elif (registerType == "3"):
            registerClient()
        elif (registerType == "x"):
            break
        else:
            registerType = ""
            print("Wrong input, enter one of the 4 inputs below")