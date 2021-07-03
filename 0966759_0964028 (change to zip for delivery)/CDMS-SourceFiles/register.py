
import database

cities = ["Rotterdam", "Amsterdam", "Den Haag", "Eindhoven","Maastricht","Delft","Breda","Haarlem","Utrecht","Leiden"]

def registerUser():
    registerType = ""
    while registerType == "":
        print("\nWhat type of user do you want to register?")
        print("Enter 1 to register a client")
        print("Enter 2 to register an advisor")
        print("Enter 3 to register a system administrator")
        print("Enter 'x' to go back")
        registerType = input("Register type: ")
        
        if(registerType == "1"):
            registerClient()
        elif (registerType == "2"):
            registerAdvisor()
        elif (registerType == "3"):
            registerSystemAdmin()
        elif (registerType == "x"):
            break
        else:
            registerType = ""
            print("Wrong input, enter one of the 4 inputs below")






def registerClient():
    name            = input("\n1. Enter the name of the new client: ")

    print(                  "\n2. Entering the address...")
    streetName      = input("2.1. Street name: ")
    zipCode         = input("2.2. Zipcode: ")
    print(                  "2.3. City: (Choose one from the list below) ")
    for city in cities:
        print("- " + city )
    city            = input("\nCity: ")
    address = streetName + ", " + zipCode + ", " + city

    email           = input("\n3. Email address: ")
    mobile          = input("\n4. Mobile: ")

    database.addClientToDb(name,address,email,mobile)
    print("\n"+ "="*40)



    print("Client {} has been added to the database".format(name))









def registerAdvisor():
    print("advisorreg")

    
def registerSystemAdmin():
    print("sysad")