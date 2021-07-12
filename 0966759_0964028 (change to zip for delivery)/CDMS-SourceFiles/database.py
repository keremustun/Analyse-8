import sqlite3
import re
import sys

connection = sqlite3.connect('CDMS.db')
cursor = connection.cursor()


createTableClients = """CREATE TABLE IF NOT EXISTS
clients(id INTEGER PRIMARY KEY AUTOINCREMENT, Full_Name TEXT, Address TEXT, Email_Address TEXT, Mobile_Phone TEXT)"""
cursor.execute(createTableClients)

createTableAdvisors = """CREATE TABLE IF NOT EXISTS
advisors(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT COLLATE NOCASE, Password TEXT, First_Name TEXT, Last_Name TEXT, Registered_Date TEXT)"""
cursor.execute(createTableAdvisors)

createTableSystemAdmins = """CREATE TABLE IF NOT EXISTS
sysadmins(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT COLLATE NOCASE, Password TEXT, First_Name TEXT, Last_Name TEXT, Registered_Date TEXT)"""
cursor.execute(createTableSystemAdmins)


createTableLog = """CREATE TABLE IF NOT EXISTS
log(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT, Suspicious TEXT)"""
cursor.execute(createTableLog)

createTableUnreadSuspicous = """CREATE TABLE IF NOT EXISTS
unreadsuslogs(susID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT)"""
cursor.execute(createTableUnreadSuspicous)

connection.commit()
#=========================================================================================================   Register  =====================================



cities = ["Rotterdam", "Amsterdam", "Zwolle", "Eindhoven","Maastricht","Delft","Breda","Haarlem","Utrecht","Leiden"]

def registerClient():
    def addClientToDb(fn,ad,ea,mp):
        sqlargs = (Crypt(fn,5,True),Crypt(ad,5,True),Crypt(ea,5,True),Crypt(mp,5,True))
        sqlargsLog = (fn,ad,ea,mp)
        sql = "INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction("Client has been added to the database", f"Inputs: {sqlargsLog}", "No")

  

    name            = ValidateName(input(      "\n1. Enter the full name of the new client: "))
    print(                                     "\n2. Entering the address...")
    streetName      = ValidateStreetName(input("2.1. Street name: "))
    houseNumber     = ValidateHouseNumber(input(    "2.2. House Number: "))
    zipCode         = ValidateZipCode(input(   "2.3. Zipcode: "))
    print(                                     "2.4. City: (Choose one from the list below) ")

    for city in cities:
        print("- " + city )
    city = ValidateCity (input("\nCity: "), cities)
    
    address = f"({streetName} {houseNumber}, {zipCode}, {city})"
    email  = ValidateEmail (input("\n3. Email address: "))
    mobile = "+31-6-" + ValidatePhoneNumber (input("\n4. Mobile: +31-6-"))

    if name == None or streetName == None or houseNumber == None or zipCode == None or city == None or address == None or email == None or mobile == None :
        print("Something Wrong happened")
        sys.exit()
    
    if name == "" or streetName == "" or houseNumber == "" or zipCode == "" or city == "" or address == "" or email == "" or mobile == "" :
        print("Something Wrong happened")
        sys.exit()

    addClientToDb(name,address,email,mobile)
    print("\n"+ "="*40)
    print("Client '{}' has been added to the database".format(name))
    input("Enter any key to continue\n")

def registerUser(usertype):
    table = decideTable(usertype)

    def addToDb(table,un,pw,fn,ln,dt):
        sqlargs = (Crypt(un,5,True),Crypt(pw,5,True),Crypt(fn,5,True),Crypt(ln,5,True),Crypt(dt,5,True))
        sqlargsLog = (un,pw,fn,ln,dt)
        sql = f"INSERT INTO {table} (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction(f"User has been added to the {table} table", f"Inputs: {sqlargsLog}", "No")

    usernameOK = False
    while not usernameOK:
        print(f"\nRegistering an {usertype}")
        uname = ValidateUserName (input(f"\n1. Enter the username of the new {usertype}: "))
        
        if userNameTaken(uname):
            print("Username: '{}' is already taken. Try something else".format((uname)))
        else:
            usernameOK = True

    psswd            = ValidatePassWord (input(f"\n2. Enter the password for the new {usertype}: "))
    fname            = ValidateFirstName (input(f"\n3. Enter the first name of the new {usertype}: "))
    lname            = ValidateLastName (input(f"\n4. Enter the last name of the new {usertype}: "))
    from datetime import date
    date = str(date.today())
    addToDb(table,uname,psswd,fname,lname,date)
    print("\n"+ "="*40)
    print(f"{usertype} '" + uname + "' has been registered on " + date)
    input("Enter any key to continue\n")


#--------------------------------------------------------------------------------------------------------------------------------
# Authentication

def AuthenticateLogin(un, pw, logintype):
    if logintype == "3":
        if not (un == "superadmin" and pw == "Admin!23"):
            return ""
        return "superadmin"

    un = Crypt(un,5,True)
    pw = Crypt(pw,5,True)

    if logintype == "1":
        cursor.execute("SELECT * FROM advisors WHERE Username=:un AND Password=:pw",{"un":un, "pw":pw})
        userExists = cursor.fetchall()
        if (userExists) == []:
            return ""
        return "advisor"

    else:
        cursor.execute("SELECT * FROM sysadmins WHERE Username=:un AND Password=:pw",{"un":un, "pw":pw})
        userExists = cursor.fetchall()
        if (userExists) == []:
            return ""
        return "systemadmin"
    
    
        

def userNameTaken(username):
    username = Crypt(username,5,True)
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
    pw = Crypt(pw, 5, True)
    un = Crypt(un, 5, True)
    if logintypeArg == '1':
        cursor.execute("SELECT Password FROM advisors WHERE Username=:un AND Password=:pw",{"un":un,"pw":pw})
        dbPassword = cursor.fetchall()
        if dbPassword != []:
            if dbPassword[0][0] == pw:
                return True
        return False
    
    elif logintypeArg == '2':
        cursor.execute("SELECT Password FROM sysadmins WHERE Username=:un AND Password=:pw",{"un":un,"pw":pw})
        dbPassword = cursor.fetchall()
        if dbPassword != []:
            if dbPassword[0][0] == pw:
                return True
        return False


def updatePassword(newpw, un, logintypeArg):
        newpw = Crypt(newpw, 5, True)
        un = Crypt(un, 5, True)
        if logintypeArg == "1":
            cursor.execute("UPDATE advisors SET Password=:pw WHERE Username=:un",{"pw":newpw,"un":un})
            connection.commit()
        else:
            cursor.execute("UPDATE sysadmins SET Password=:pw WHERE Username=:un",{"pw":newpw,"un":un})
            connection.commit()

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
                logAction("User has updated their password", "", "No")
                return
            else:
                print("Passwords dont match")
                userInput = ''
        else:
            strikes += 1
            if strikes == 5:
                print("Incorrect password too many times. Logging out...")
                logAction("User tried to update their password", f"Password incorrect too many times, User input: {userInput}", "Yes")
                quit()
            else:
                print("Incorrect password. Please try again.")
                logAction("User tried to update their password", f"Password incorrect, user input: {userInput}", "No")
                userInput = ''


def resetPassword(logintypeArg):
    usertype = ""
    if logintypeArg == "1":
        usertype = "advisor"
    else:
        usertype = "system admin"

    table = decideTable(usertype)

    choicedesc = f"Enter the username of the {usertype} who's password you want to reset\nOR\nEnter 'list' to list all {usertype}s\nOR\nEnter 'x' to exit\n\n"
    choice = input(choicedesc)

    success = False
    while not success:
        print("\n\n")
        if choice == 'x':
            return
        elif choice == 'list':
            getColumns(table, False)
            rows = showAllFromTable(table)
            for row in rows:
                print(row)
            print("=" * 80)
            choice = input(f"\nEnter the username of the {usertype} who's password you want to reset\nOR\nEnter 'x' to exit\n\n")
        else: 
                newPass        = ValidatePassWord(input("Enter the new password: "))
                confirmNewPass = input("Enter the new password again for confirmation: ")
                if newPass == confirmNewPass:
                    updatePassword(confirmNewPass, choice, logintypeArg)
                    logAction(f"{usertype} password updated", f"{choice}'s password has been updated", "No")
                    print("Password has been succesfully updated!")
                    return
                else:
                    print("Passwords dont match")

def showSus():
    choice = '' 
    while choice != 'x':
        rows = showAllFromTable("unreadsuslogs")
        getColumns("unreadsuslogs", False)
        for row in rows:
            print(row)
        print("=" * 70)
        logAction("Display suspicious activites", "", "No")

        choicedesc = "Enter the id of suspicious activity to mark it as read\nOR\nEnter'x' to exit\n\n"
        choice = input(choicedesc)
        if choice != 'x':
            if not str.isdigit(choice):
                logAction("Attempt to mark suspicious activity as read", f"id input: {choice}", "Yes")
                return
            else:
                cursor.execute("SELECT * FROM unreadsuslogs WHERE susID=:id",{"id":choice})
                susdesc = cursor.fetchall()

                cursor.execute(f"DELETE FROM unreadsuslogs WHERE susID=:id",{"id":choice})
                connection.commit()
                logAction("Suspicious activity marked as read", f"Suspicious activity info: {susdesc}", "No")
                print("\n" * 40)
            return


def showAllFromTable(tablename):
    sql = f"SELECT * FROM {tablename}"
    cursor.execute(sql)
    results = cursor.fetchall()
    decResults = []

    if tablename in ["advisors","sysadmins"]:
        for row in results:
            record = []
            for index, i in enumerate(row):
                if index == 2:
                    record.append("*private*")
                else:
                    record.append(Crypt(i, 5, False))
            decResults.append(record)
        return decResults

    else:
        for row in results:
            record = []
            for i in row:
                record.append(Crypt(i, 5, False))
            decResults.append(record)
        return decResults

def getColumns(tableName,allusers):
    cursor.execute("PRAGMA table_info({})".format(tableName))
    tableInfo = cursor.fetchall()
    columns = ''
    if allusers:
        columns = "=" * 120 + "\nTable Name: All System Users\nColumns:\n"
        currentColumn = 0
        allUserColumns = ['id', 'Role', 'Username']
        for column in allUserColumns:
            if currentColumn != (len(tableInfo)-1):
                columns += column + ", "
            else:
                columns += column
            currentColumn += 1
    else:
        columns = "=" * 120 + "\nTable Name: {}\nColumns:\n".format(tableName)
        currentColumn = 0
        for column in tableInfo:
            if currentColumn != (len(tableInfo)-1):
                columns += column[1] + ", "
            else:
                columns += column[1]
            currentColumn += 1
    print("\n"*30)
    print(columns)
    print("-"*120)


def getRecordInfo(table,idarg):
    cursor.execute(f"SELECT * FROM {table} WHERE id=:id",{"id":idarg})
    results = cursor.fetchall()
    if results == []:
        logAction(f"User searched for record in {table} table", f"Nothing found, user input: {idarg}", "No")
        return []

    if str.isdigit(idarg):
        logAction(f"User searched for record in {table} table", f"User input for client's id: {idarg}", "No")
    else:
        logAction(f"User searched for record in {table} table", f"User input for client's id: {idarg}", "Yes")
    
    
    dec  = []
    row = results[0]
    for column in row:
        dec.append(Crypt(column, 5, False))
    
    decResults = []
    decResults.append(dec)
    return decResults




def getUser(username, password, logintypeArg):
    if logintypeArg == '1':
        cursor.execute("SELECT * FROM advisors WHERE Username=:username AND Password=:password",{"username":username, "password":password})
    else:
        cursor.execute("SELECT * FROM sysadmins WHERE Username=:username AND Password=:password",{"username":username, "password":password})
    results = cursor.fetchall()
    return results


def decideTable(usertype):
    table = ""
    if usertype == "client":
        table = "clients"
    elif usertype == "advisor":
        table = "advisors"
    elif usertype == "system admin":
        table = "sysadmins"
    print("\n" * 30)
    return table

def modRecord(usertype):
    table = decideTable(usertype)

    #DONT CHANGE THE INDENTATION HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    uid = input(f"Enter the id of the {usertype} who's info you want to update\n\
Or\n\
Enter 'list' to show the list of all {usertype}s and their id's\n\
Or\n\
Enter 'x' to exit\n\n")

    if uid == 'x':
      return
    elif uid == 'list':
        rows = showAllFromTable(table)
        getColumns(table,False)
        for row in rows:
            rowText = ""
            for index, column in enumerate(row):
                if index < len(row) -1:
                    rowText += column  + ", "
                else:
                    rowText += column
            print(rowText + " | END OR ROW | ")

        print("="*120)
        input("Enter any key to continue")
    else:
        info = getRecordInfo(table, uid)
        if info == []:
            print(f"{usertype} doesn't exist")
        else:
            print("\n" * 40)
            getColumns(table,False)
            if table in ["advisors","sysadmins"]:
                info[0][2] = "*private*"
            print(f"{usertype} info: " + str(info[0]))
            print("="*120)

            columnList = []
            while True:
                columnName = input("Enter the name of the column that you want to modify: ")
                cursor.execute("PRAGMA table_info({})".format(table))
                tableInfo = cursor.fetchall()
                for row in tableInfo:
                    columnList.append(row[1])
                if columnName in columnList:
                    break
                print("Column doesn't exist")
            
            newInfo = ""
            if usertype == "client":
                if columnName == "Full_Name":
                    newInfo = ValidateName(input("Enter the new name: "))
                elif columnName == "Address":
                    streetName = ValidateStreetName((input("Enter the street name: ")))
                    houseNumber = ValidateHouseNumber((input("Enter the house number: ")))
                    zipCode = ValidateZipCode((input("Enter the zipcode: ")))
                    print("\nChoose a city from below")
                    for city in cities:
                        print("- " + city )
                    city = ValidateCity(input("\nEnter the city: "), cities)
    
                    newInfo = f"({streetName} {houseNumber}, {zipCode}, {city})"
                elif columnName == "Email_Address":
                    newInfo = ValidateEmail (input("\nEnter the new email adress: "))
                elif columnName == "Mobile_Phone":
                    newInfo = "+31-6-" + ValidatePhoneNumber (input("\nEnter the new phone number:"))
                else:
                    print(f"You cannot modify the data in column: {columnName}")
                    input("Enter any key to continue ")
                    return
            
            else:
                if columnName == "Username":
                    newInfo = ValidateUserName (input(f"Enter the new username: "))
                elif columnName == "Password":
                    newInfo = ValidatePassWord(input(f"Enter the new password: "))
                elif columnName == "First_Name":
                    newInfo = ValidateFirstName(input(f"Enter the new first name: "))
                elif columnName == "Last_Name":
                    newInfo = ValidateLastName(input(f"Enter the new last name: "))
                else:
                    print(f"You cannot modify the data in column: {columnName}")
                    input("Enter any key to continue ")
                    return

            updateInfo(columnName,table,newInfo,uid)
            input("Enter any key to continue\n")

def updateInfo(columnName,table,newInfo,uid):
    sql = f"UPDATE {table} SET {columnName} = ? WHERE id = ?"
    args = (Crypt(newInfo,5,True),uid)
    cursor.execute(sql,args)
    connection.commit()
    if columnName == "Password":
        newInfo = len(newInfo) *  "*"
    logAction(f"Info in {table} table updated", f"Column {columnName} at id: {uid} changed to {newInfo}", "No")
    print("Update successful")

def searchRecord(usertype):
    table = decideTable(usertype)
    print("\n" * 30)

    #DONT CHANGE THE INDENTATION HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    uid = input(f"Enter the id of the {usertype} who's info you want to retrieve\n\
Or\n\
Enter 'list' to show the list of all {usertype}s and their info\n\
Or\n\
Enter 'x' to exit\n\n")

    if uid == 'x':
      return
    elif uid == 'list':
        rows = showAllFromTable(table)
        getColumns(table,False)
        for row in rows:
            print(row)
        print("="*80)
        input("Enter any key to continue")
    else:
        info = getRecordInfo(table, uid)
        if info == []:
            print(f"{usertype} doesn't exist")
        else:
            print("\n" * 40)
            getColumns(table,False)
            print(f"{usertype} info: " + str(info[0]))
            print("="*80)
            input("Enter any key to continue")


def deleteRecord(usertype):
    table = decideTable(usertype)
    def deleteRecord2(usertype,table,uid):
        info = getRecordInfo(table, uid)
        if info == []:
            print("\n" * 40)
            print(f"{usertype} with id '{uid}' doesn't exist\n")
            if not str.isdigit(uid):
                logAction(f"Attempt to delete: {usertype}",f"Input:{uid}","Yes")
        else:
            cursor.execute(f"DELETE FROM {table} WHERE id=:id",{"id":uid})
            connection.commit()
            print("\n" * 40)
            print(f"{uid} '{info[0][1]}' with id:{info[0][0]} has been deleted\n")
            logAction(f"{usertype} deleted", f"'{info[0][1]}' with id:{info[0][0]} has been deleted", "No")
            return

    print("\n" * 30 + f"\nSo you want to delete a {usertype} huh?\nThen you've come to the right place\n")
    #DONT CHANGE THE INDENTATION HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    uid = ''
    while uid != 'x':
        uid = input(f"Enter the id of the {usertype} who you want to delete\n\
Or\n\
Enter 'list' to show the list of all {usertype}s and their id's\n\
Or\n\
Enter 'x' to exit\n\n\
Choice: ")

        if uid == 'x':
            return

        elif uid == 'list':
            rows = showAllFromTable(table)
            getColumns(table,False)
            for row in rows:
                print(row)
            print("="*80)
            uid = input(f"Enter the id of the {usertype} to delete OR enter 'x' to exit: ")
            if uid == "x":
                return

            if uid != 'list':
                deleteRecord2(usertype, table, uid)
                
        else:
            deleteRecord2(usertype, table, uid)
            


def listAllUsers():
    print("\n" * 30)
    getColumns('advisors',True)

    print("'SuprAdmID:0', 'Super Admin', 'superadmin' | END OF ROW |")
    print("~"*80)
    cursor.execute("SELECT ('AdvisorID:' || id) as id , 'Advisor' as Role, Username FROM advisors")
    advisors = cursor.fetchall()
    for advisor in advisors:
        record = ""
        for index, column in enumerate(advisor):
            if index < len(advisor) - 1:
                record += column + ", "
            else:
                record += Crypt(column, 5, False) + " | END OF ROW |"
        print(record)
    print("~"*80)
    cursor.execute("SELECT ('SystAdmID:' || id) as id , 'System Admin' as Role, Username FROM sysadmins")
    sysadmins = cursor.fetchall()
    for sysadmin in sysadmins:
        record = ""
        for index, column in enumerate(sysadmin):
            if index < len(sysadmin) - 1:
                record += column + ", "
            else:
                record += Crypt(column, 5, False) + " | END OF ROW |"
        print(record)
    print("="*80)
    logAction("Listed all employees", "", "No")
    input("Enter any key to exit\n")
   

def logAction(dc,ad,sp):
    from currentuser import currentUserName
    username = Crypt(currentUserName,5,True)

    from datetime import date, datetime
    date = str(date.today())
    date = Crypt(date,5,True)
    
    time = str((datetime.now()).strftime("%H:%M:%S"))
    time = Crypt(time,5,True)

    desc = Crypt(dc, 5, True)
    if ad == "":
        ad = "No additional information"
    addinfo = Crypt(ad, 5, True)
    sus = Crypt(sp, 5, True)

    sql = """INSERT INTO log (Username, Date, Time, Description_of_activity, Additional_information, Suspicious)
                      VALUES (?,?,?,?,?,?)"""
    args = (username,date,time,desc,addinfo,sus)
    cursor.execute(sql,args) 
    connection.commit() 

    if Crypt(sus, 5, False) == "Yes":
        
        sql = """INSERT INTO unreadsuslogs (Username, Date, Time, Description_of_activity, Additional_information)
        VALUES (?,?,?,?,?)"""
        args = (username,date,time,desc,addinfo)
        cursor.execute(sql,args)
        connection.commit()

    
def checkForSus():
    sql = """SELECT COUNT(*) FROM unreadsuslogs"""
    cursor.execute(sql)
    res = cursor.fetchall()    
    return res[0][0]

def show_log():
    print("\n"*30)
    cursor.execute("SELECT * FROM log")
    rows = cursor.fetchall()
    getColumns("log", False)
    for row in rows:
        rowtext = ""
        for index, i in enumerate(row):
            if index < len(row) - 1:
                rowtext += Crypt(i, 5, False) + ", "
            else:
                rowtext += Crypt(i, 5, False) 
        print(rowtext + " |ROW END| ")

    print("="* 100)
    logAction("Displayed logs", "", "No")
    input("\nEnter any key to continue ")


def empty_table():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    res = cursor.fetchall()
    tables = []
    for i in res:
        tables.append(i[0])

    name = ""
    while True:    
        name = input("Empty table. Tablename: ")
        if name in tables:
            if name != "sqlite_sequence":
                break
        print("Invalid input")

    cursor.execute(f"DELETE FROM {name}")
    connection.commit()

def drop_table():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    res = cursor.fetchall()
    tables = []
    for i in res:
        tables.append(i[0])

    name = ""
    while True:    
        name = input("Drop table. Tablename: ")
        if name in tables:
            if name != "sqlite_sequence":
                break
        print("Invalid input")

    cursor.execute(f"DROP TABLE {name}")
    connection.commit()
    


def ValidateName (name):
    while not re.match('^([a-zA-Z\']{1,40})+\ +([a-zA-Z]{1,40})+$', name):
        name = input("Please enter a valid full name (Firstname and lastname with a space between them): ")
        logAction("Invalid name input", f"Input: {name}", "No")
    return name

def ValidateStreetName (streetname):
    while not re.match('^([a-zA-Z]{1,50})+$', streetname.replace(" ","")): 
        streetname = input("Please enter a valid street name: ")
        logAction("Invalid street name input", f"Input: {streetname}", "No")
    return streetname

def ValidateHouseNumber (housenumber):
    while not re.match('^([a-zA-Z0-9]{1,20})+$', housenumber):
        housenumber = input("Please enter a valid house number: ")
        logAction("Invalid house number input", f"Input: {housenumber}", "No")
    return housenumber

def ValidateZipCode (zipcode):
    while not re.match("^[0-9]{4}([a-zA-Z]{2})$", zipcode):
        zipcode = input("Please enter a valid zipcode (zipcode should be 4 numbers and 2 letters with no space): ")
        logAction("Invalid zipcode input", f"Input: {zipcode}", "No")
    return zipcode

def ValidateEmail (email):
    while not re.match('^([A-Za-z0-9._%+-]{2,40})+@([A-Za-z0-9.-]{2,20})+\.[A-Z|a-z]{2,}$', email):  
        email = input("Please enter a valid email address: ")
        logAction("Invalid email input", f"Input: {email}", "No")
    return email

def ValidatePhoneNumber (mobile):
    while not re.match('^[0-9]{8}$', mobile):  
       mobile = input("Please enter a valid phone number: +31-6-")
       logAction("Invalid phonenumber input", f"Input: {mobile}", "No")
    return mobile
    
def ValidateCity (city, cities):
    strikes = 0
    while city not in cities:
        strikes += 1

        if strikes == 2:
            print("Invalid input. Incident Logged")
            logAction("Invalid city input", f"Input: {city}", "Yes")
            exit()

        logAction("Invalid city input", f"Input: {city}", "No")
        print ("Please choose one from the list below:")
        for city in cities:
            print("- " + city )
        city = input("\nCity: ")
    return city

def ValidateUserName (username):
    while not re.match('^([A-Za-z]{1})+([A-Za-z0-9._\'-]{4,19})$', username):  
        username = input("Please enter a valid username\n- Must have a length of at least 5 characters\n- Must be no longer than 20 characters\n- Must start with a letter\n- Can contain letters, numbers, (-), (_), (') and (.))\n\nUsername:")
        logAction("Invalid username input", f"Input: {username}", "No")
    return username

def ValidatePassWord (password):
    while not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&/~#^+_=`|:;\'<>,.)(}{-])[A-Za-z\d@$!%*?&/~#^+_=`|:;\'<>,.)(}{-]{8,}$", password):  
        password = input("Please enter a valid password\n- Must have a length of at least 8 characters\n- Must be no longer than 30 characters\n- Must have a combination of at least one lowercase letter, one uppercase letter, one digit and one special character\n\nPassword: ")
        logAction("Invalid password input", f"Input: {password}", "No")
    return password 

def ValidateFirstName (firstname):
    while not re.match('^([a-zA-Z\']{1,40})+$', firstname):
        firstname = input("Please enter a valid first name: ")
        logAction("Invalid first name input", f"Input: {firstname}", "No")
    return firstname

def ValidateLastName (lastname):
    while not re.match('^([a-zA-Z\']{1,40})+$', lastname):
        lastname = input("Please enter a valid last name: ")
        logAction("Invalid last name input", f"Input: {lastname}", "No")
    return lastname


def Crypt(text, key, encrypt):
    if isinstance(text, int):
        return str(text)
    import string
    characters = string.ascii_letters + string.digits + " " + string.punctuation
    #print("Extended character set: " + characters)
    if key < 0:
        print("Key cannot be negative")
        return None
    
    n = len(characters)

    if not encrypt:
        key = n - key

    table = str.maketrans(characters, characters[key:]+characters[:key])

    translated_text = text.translate(table)
    return translated_text

    # plain_text = "My name is Dave Adams. I am living on the 99th street. Please send the supplies!"
    # x = cipher_wlookup(plain_text, 15, True)
    # print(x)
    # z = cipher_wlookup(x, 15, False)
    # print(z)



def Backup():
    def progress(status, remaining, total):
        print(f"Copied {total-remaining} of {total} pages...")

    
    logAction("Backup created", "", "No")
    dest = sqlite3.connect('backup.db')
    with dest:
        connection.backup(dest, pages=1, progress=progress)
    
    dest.close()

    import zipfile,os
    if os.path.exists('backup.zip'):
        os.remove('backup.zip')

    backup = zipfile.ZipFile('backup.zip','a') 
    backup.write('backup.db')
    backup.close()

    os.remove('backup.db')
    

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
