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
    print("\n" * 30)
    registerType = ""
    while registerType == "":
        print("\nWhat type of user do you want to register?")
        print("Enter 1 to register a client")
        print("Enter 2 to register an advisor")
        print("Enter 3 to register a system administrator")
        print("Enter 'x' to go back")
        registerType = input("Register type: ")
        print("\n" * 30)
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
    def addSystemAdminToDb(un,pw,fn,ln,dt):
        sqlargs = (un,pw,fn,ln,dt)
        sql = "INSERT INTO sysadmins (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
   
    usernameOK = False
    while not usernameOK:
        print("Registering an system admin. Enter 'q' to quit OR")
        uname = input("\n1. Enter the username of the new system admin: ")
        if uname == 'q':
            return
        if userNameTaken(uname):
            print("\n" * 30)
            print("Username: '{}' is already taken. Try something else".format((uname)))
        else:
            print("-  Username '{}' is available".format(uname))
            usernameOK = True

    psswd            = input("\n2. Enter the password for the new system admin: ")
    fname            = input("\n3. Enter the first name of the new system admin: ")
    lname            = input("\n4. Enter the last name of the new system admin: ")
    from datetime import date
    date = str(date.today())
    addSystemAdminToDb(uname,psswd,fname,lname,date)
    print("System admin " + uname + " has been registered on " + date)



#--------------------------------------------------------------------------------------------------------------------------------
# Authentication

def AuthenticateLogin(un, pw, logintype):
    if logintype == "1":
        cursor.execute("SELECT * FROM advisors WHERE Username=:un AND Password=:pw",{"un":un, "pw":pw})
        userExists = cursor.fetchall()
        if (userExists) == []:
            return ""
        return "advisor"

    elif logintype == "2":
        cursor.execute("SELECT * FROM sysadmins WHERE Username=:un AND Password=:pw",{"un":un, "pw":pw})
        userExists = cursor.fetchall()
        if (userExists) == []:
            return ""
        return "systemadmin"
    
    else:
        if not (username == "superadmin" and password == "Admin!23"):
            return ""
        return "superadmin"
        

def userNameTaken(username):
    cursor.execute("SELECT * FROM advisors WHERE Username=:username",{"username":username})
    advisorUserNameInDb = cursor.fetchall()
    if advisorUserNameInDb != []:
        return True

    cursor.execute("SELECT * FROM sysadmins WHERE Username=:username",{"username":username})
    sysadminUserNameInDb = cursor.fetchall()
    if sysadminUserNameInDb != []:
        return True
    return False
#--------------------------------------------------------------------------------------------------------------------------------
# Advisor functions

def authenticatePassword(pw, un, logintypeArg):
    if logintypeArg == '1':
        cursor.execute("SELECT Password FROM advisors WHERE Username=:un AND Password=:pw",{"un":un,"pw":pw})
        dbPassword = cursor.fetchall()
        if dbPassword != []:
            if dbPassword[0][0] == pw:
                return True
        return False
    
    if logintypeArg == '2':
        cursor.execute("SELECT Password FROM sysadmins WHERE Username=:un AND Password=:pw",{"un":un,"pw":pw})
        dbPassword = cursor.fetchall()[0][0]
        if dbPassword == pw:
            return True
        return False








def changePassword(un,logintypeArg):
        userInput = ''
        strikes = 0
        while userInput == '': 
            userInput = input("Enter your current password or enter 'x' to exit:\n")
            if userInput == 'x':
                return

            correctPassword = authenticatePassword(userInput, un, logintypeArg)
            if correctPassword:
                newPass        = input("Enter the new password: ")
                confirmNewPass = input("Enter the new password again for confirmation: ")
                if newPass == confirmNewPass:
                    updatePassword(newPass, un, logintypeArg)
                    print("Password has been succesfully updated!")
                    return
                else:
                    print("Passwords dont match")
                    userInput = ''
            else:
                strikes += 1
                if strikes == 3:
                    print("Incorrect password too many times. Logging out...")
                    quit()
                else:
                    print("Incorrect password. Please try again.")
                    userInput = ''


def updatePassword(newpw, un, logintypeArg):
    if logintypeArg == "1":
        updatePassSQL = "UPDATE advisors SET Password = ? WHERE Username = ?"
        args = (newpw, un)
        cursor.execute(updatePassSQL,args)
        connection.commit()
    else:
        updatePassSQL = "UPDATE sysadmins SET Password = ? WHERE Username = ?"
        args = (newpw, un)
        cursor.execute(updatePassSQL,args)
        connection.commit()
    





def showAllClients():
    cursor.execute("SELECT * FROM clients")
    results = cursor.fetchall()
    return results

def getColumns(tableName):
    cursor.execute("PRAGMA table_info({})".format(tableName))
    tableInfo = cursor.fetchall()
    columns = "=" * 80 + "\nTable Name: {}\nColumns:\n".format(tableName)
    currentColumn = 0
    for column in tableInfo:
        if currentColumn != (len(tableInfo)-1):
            columns += column[1] + ", "
        else:
            columns += column[1]
        currentColumn += 1
    print("\n"*30)
    print(columns)
    print("-"*80)


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



def modClient():
    print("\n" * 30)

    #DONT CHANGE THE INDENTATION HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    clientId = input("Enter the id of the client who's info you want to update\n\
Or\n\
Enter 'list' to show the list of all clients and their id's\n\
Or\n\
Enter 'x' to exit\n\n")

    if clientId == 'x':
      return
    elif clientId == 'list':
        allClients = showAllClients()
        getColumns("clients")
        for client in allClients:
            print(client )
        print("="*80)
    else:
        clientInfo = getClientInfo(clientId)
        if clientInfo == []:
            print("Client doesn't exist")
        else:
            print("\n" * 40)
            getColumns("clients")
            print("Client info: " + str(clientInfo[0]))
            print("="*80)

            columnName = input("Enter the name of the column that you want to modify: ")
            newInfo = input("Enter the new info:")
            updateInfo(columnName,newInfo,clientId)


def updateInfo(columnName,newInfo,uid):
    sql = "UPDATE clients SET {} = ? WHERE id = ?".format(columnName)
    args = (newInfo,uid)
    cursor.execute(sql,args)
    connection.commit()
    print("Update successful")

def searchClient():
    print("\n" * 30)

    #DONT CHANGE THE INDENTATION HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    clientId = input("Enter the id of the client who's info you want to retrieve\n\
Or\n\
Enter 'list' to show the list of all clients and their info\n\
Or\n\
Enter 'x' to exit\n\n")

    if clientId == 'x':
      return
    elif clientId == 'list':
        allClients = showAllClients()
        getColumns("clients")
        for client in allClients:
            print(client )
        print("="*80)
    else:
        clientInfo = getClientInfo(clientId)
        if clientInfo == []:
            print("Client doesn't exist")
        else:
            print("\n" * 40)
            getColumns("clients")
            print("Client info: " + str(clientInfo[0]))
            print("="*80)


def drop_table():
    name = input("delete content of table. tablename: ")
    cursor.execute("DELETE FROM {}".format(name))
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


def Encrypt(text):
    result = ""
    shift = 5
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for char in text:
        if char in alpha:
            index = (alpha.find(char) + shift) % len(alpha)
            result += alpha[index]
        else:
            result += char
    return result


def Decrypt (text):
    result = ""
    shift = 5
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for char in text:
        if char in alpha:
            index = (alpha.find(char) - shift) % len(alpha)
            result += alpha[index]
        else:
            result += char
    return result


