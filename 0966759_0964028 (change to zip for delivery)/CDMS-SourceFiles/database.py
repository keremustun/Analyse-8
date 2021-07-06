import sqlite3
import re
import sys

connection = sqlite3.connect('CDMS.db')
cursor = connection.cursor()


createTableClients = """CREATE TABLE IF NOT EXISTS
clients(id INTEGER PRIMARY KEY AUTOINCREMENT, Full_Name TEXT, Address TEXT, Email_Address TEXT, Mobile_Phone TEXT)"""
cursor.execute(createTableClients)

createTableAdvisors = """CREATE TABLE IF NOT EXISTS
advisors(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, First_Name TEXT, Last_Name TEXT, Registered_Date TEXT)"""
cursor.execute(createTableAdvisors)

createTableSystemAdmins = """CREATE TABLE IF NOT EXISTS
sysadmins(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, First_Name TEXT, Last_Name TEXT, Registered_Date TEXT)"""
cursor.execute(createTableSystemAdmins)


createTableLog = """CREATE TABLE IF NOT EXISTS
log(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Description_of_activity TEXT, Additional_information TEXT, Suspicious TEXT)"""
cursor.execute(createTableLog)


#=========================================================================================================   Register  =====================================



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
    def addClientToDb(fn,ad,ea,mp):
        print("registering client...")
        sqlargs = (fn,ad,ea,mp)
        sql = "INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()

    cities = ["Rotterdam", "Amsterdam", "Den Haag", "Eindhoven","Maastricht","Delft","Breda","Haarlem","Utrecht","Leiden"]

    name            = ValidateName(input(      "\n1. Enter the full name of the new client: "))
    print(                                     "\n2. Entering the address...")
    streetName      = ValidateStreetName(input("2.1. Street name: "))
    houseNumber     = ValidateHouseNumber(input(    "2.2. Houser Number: "))
    zipCode         = ValidateZipCode(input(   "2.3. Zipcode: "))
    print(                                     "2.4. City: (Choose one from the list below) ")

    for city in cities:
        print("- " + city )
    city = ValidateCity (input("\nCity: "), cities)
    
    address = f"{streetName} {houseNumber}, {zipCode}, {city}"
    email  = ValidateEmail (input("\n3. Email address: "))
    mobile =ValidatePhoneNumber (input("\n4. Mobile: +31-6-"))

    if name == None or streetName == None or houseNumber == None or zipCode == None or city == None or address == None or email == None or mobile == None :
        print("Something Wrong happened")
        sys.exit()
    
    if name == "" or streetName == "" or houseNumber == "" or zipCode == "" or city == "" or address == "" or email == "" or mobile == "" :
        print("Something Wrong happened")
        sys.exit()

    addClientToDb(name,address,email,mobile)
    print("\n"+ "="*40)
    print("Client {} has been added to the database".format(name))


def registerAdvisor():
    def addAdvisorToDb(un,pw,fn,ln,dt):
        print("registering advisor...")
        sqlargs = (un,pw,fn,ln,dt)
        sql = "INSERT INTO advisors (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()

    usernameOK = False
    while not usernameOK:
        print("\nRegistering an advisor. Enter 'q' to quit OR")
        uname = input("\n1. Enter the username of the new advisor: ")
        if uname == 'q':
            return
        if userNameTaken(uname):
            print("Username: '{}' is already taken. Try something else".format((uname)))
        else:
            usernameOK = True

    psswd            = input("\n2. Enter the password for the new advisor: ")
    fname            = input("\n3. Enter the first name of the new advisor: ")
    lname            = input("\n4. Enter the last name of the new advisor: ")
    from datetime import date
    date = str(date.today())
    addAdvisorToDb(uname,psswd,fname,lname,date)
    print("Advisor " + uname + " has been registered on " + date)




def registerSystemAdmin():
    def addSystemAdminToDb(fn,ad,ea,mp):
        print("registering system admin...")
        sqlargs = (un,pw,fn,ln,dt)
        sql = "INSERT INTO sysadmins (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
    print("sysad")

#--------------------------------------------------------------------------------------------------------------------------------
# Authentication

def AuthenticateLogin(username, password, logintype):
    if logintype == "3":
        if username == "superadmin" and password == "Admin!23":
            return "superadmin"
    elif logintype == "2":
        cursor.execute("SELECT * FROM sysadmins WHERE id=:id",{"id":idarg})


def userNameTaken(username):
    cursor.execute("SELECT * FROM advisors WHERE Username=:username",{"username":username})
    advisorUserNameInDb = cursor.fetchall()
    if advisorUserNameInDb != []:
        return True

    cursor.execute("SELECT * FROM sysadmins WHERE Username=:username",{"username":username})
    sysadminUserNameInDb = cursor.fetchall()
    if sysadminUserNameInDb != []:
        return True

    print("username available")
    return False
#--------------------------------------------------------------------------------------------------------------------------------
# Advisor functions

# def authenticatePassword():
#     x

# def updatePassword():
#     x

def showAllClients():
    cursor.execute("SELECT * FROM clients")
    results = cursor.fetchall()
    return results

def getColumns(tableName):
    cursor.execute("PRAGMA table_info(?)",tableName)

def getClientInfo(idarg):
    cursor.execute("SELECT * FROM clients WHERE id=:id",{"id":idarg})
    results = cursor.fetchall()
    return results

def getUser(username, password, logintypeArg):
    if logintypeArg == '1':
        cursor.execute("SELECT * FROM advisors WHERE Username=:username AND Password=:password",{"username":username, "password":password})
    else:
        cursor.execute("SELECT * FROM sysadmins WHERE Username=:username AND Password=:password",{"username":username, "password":password})
    results = cursor.fetchall()
    return results



connection.commit()




#FOREIGN KEY(store_id) REFERENCES stores(store_id)) (reminder on how to do foreign keys)

#--------------INSERT INTO CLIENT
# cursor.execute("INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone)\
#                             VALUES  ('Bob','Afri','Afri@gmail.com','124142142' )")
# cursor.execute("INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone)\
#                             VALUES  ('Boasdb','Afasdri','Afriasdgmail.com','124142asd142' )")

# cursor.execute("UPDATE purchases SET total_cost = 3.67 WHERE purchase_id = 2")
# cursor.execute("DELETE FROM purchases WHERE purchase_id = 3")

# sqlinjection="Bob' OR 'a' = 'a' --"

# #injection prevented

#cursor.execute("SELECT * FROM clients WHERE id=:id",{"id":fn})
#cursor.execute("SELECT * FROM clients WHERE Full_Name='{}'".format(fn))

# cursor.execute("SELECT * FROM clients WHERE Full_Name=:username",{"username":bob})

#injection unprevented
#cursor.execute("SELECT * FROM clients WHERE Full_Name='{}'".format(bob))


def ValidateName (name):
    while not re.match('^([a-zA-Z]{1,40})+\ +([a-zA-Z]{1,40})+$', name):
        name = input("Please enter a valid full name (Firstname and lastname with a space between them): ")
    return name

def ValidateStreetName (streetname):
    while not re.match('^([a-zA-Z]{1,50})+$', streetname.replace(" ","")): 
        streetname = input("Please enter a valid street name: ")
    return streetname

def ValidateHouseNumber (housenumber):
    while not re.match('^([a-zA-Z0-9]{1,20})+$', housenumber):
        housenumber = input("Please enter a valid house number: ")
    return housenumber

def ValidateZipCode (zipcode):
    while not re.match("^[0-9]{4}([a-zA-Z]{2})$", zipcode):
        zipcode = input("Please enter a valid zipcode (zipcode should be 4 numbers and 2 letters with no space): ")
    return zipcode

def ValidateEmail (email):
    while not re.match('^([A-Za-z0-9._%+-]{2,40})+@([A-Za-z0-9.-]{2,20})+\.[A-Z|a-z]{2,}$', email):  
        email = input("Please enter a valid email address: ")
    return email

def ValidatePhoneNumber (mobile):
    while not re.match('^[0-9]{8}$', mobile):  
       mobile = input("Please enter a valid phone number: +31-6-")
    return mobile
    
def ValidateCity (city, cities):
    while city not in cities:
        print ("Please choose one from the list below:")
        for city in cities:
            print("- " + city )
        city = input("\nCity: ")
    return city