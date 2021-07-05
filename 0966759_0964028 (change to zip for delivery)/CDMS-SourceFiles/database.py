import sqlite3

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
    def addClientToDb(fn,ad,ea,mp):
        print("registering client...")
        sqlargs = (fn,ad,ea,mp)
        sql = "INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()

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

def drop_table():
    name = input("delete content of table. tablename: ")
    cursor.execute("DELETE FROM {}".format(name))
    connection.commit()
    

drop_table()


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