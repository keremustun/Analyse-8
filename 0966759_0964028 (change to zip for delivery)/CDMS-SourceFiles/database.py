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
log(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT, Suspicious TEXT)"""
cursor.execute(createTableLog)

createTableUnreadSuspicous = """CREATE TABLE IF NOT EXISTS
unreadsuslogs(susID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT)"""
cursor.execute(createTableUnreadSuspicous)

connection.commit()
#=========================================================================================================   Register  =====================================





def registerClient():
    def addClientToDb(fn,ad,ea,mp):
        sqlargs = (fn,ad,ea,mp)
        sql = "INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction("Client has been added to the database", f"Inputs: {sqlargs}", "No")

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
    
    address = Encrypt (f"{streetName} {houseNumber}, {zipCode}, {city}")
    email  = Encrypt (ValidateEmail (input("\n3. Email address: ")))
    mobile = Encrypt (ValidatePhoneNumber (input("\n4. Mobile: +31-6-")))

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
        sqlargs = (Encrypt(un),Encrypt(pw),Encrypt(fn),Encrypt(ln),dt)
        sql = f"INSERT INTO {table} (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction(f"User has been added to the {table} table", f"Inputs: {sqlargs}", "No")

    usernameOK = False
    while not usernameOK:
        print(f"\nRegistering an {usertype}. Enter 'q' to quit OR")
        uname = input(f"\n1. Enter the username of the new {usertype}: ")
        if uname == 'q':
            return
        if userNameTaken(uname):
            print("Username: '{}' is already taken. Try something else".format((uname)))
        else:
            usernameOK = True

    psswd            = input(f"\n2. Enter the password for the new {usertype}: ")
    fname            = input(f"\n3. Enter the first name of the new {usertype}: ")
    lname            = input(f"\n4. Enter the last name of the new {usertype}: ")
    from datetime import date
    date = str(date.today())
    addToDb(table,uname,psswd,fname,lname,date)
    print("\n"+ "="*40)
    print(f"{usertype} '" + uname + "' has been registered on " + date)
    input("Enter any key to continue\n")


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
        if not (un == "superadmin" and pw == "Admin!23"):
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
    
    elif logintypeArg == '2':
        cursor.execute("SELECT Password FROM sysadmins WHERE Username=:un AND Password=:pw",{"un":un,"pw":pw})
        dbPassword = cursor.fetchall()
        if dbPassword != []:
            if dbPassword[0][0] == pw:
                return True
        return False


def updatePassword(newpw, un, logintypeArg):
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
                newPass        = input("Enter the new password: ")
                confirmNewPass = input("Enter the new password again for confirmation: ")
                if newPass == confirmNewPass:
                    updatePassword(newPass, choice, logintypeArg)
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
    return results

def getColumns(tableName,allusers):
    cursor.execute("PRAGMA table_info({})".format(tableName))
    tableInfo = cursor.fetchall()
    columns = ''
    if allusers:
        columns = "=" * 80 + "\nTable Name: All System Users\nColumns:\n"
        currentColumn = 0
        allUserColumns = ['id', 'Role', 'Username']
        for column in allUserColumns:
            if currentColumn != (len(tableInfo)-1):
                columns += column + ", "
            else:
                columns += column
            currentColumn += 1
    else:
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


def getRecordInfo(table,idarg):
    cursor.execute(f"SELECT * FROM {table} WHERE id=:id",{"id":idarg})
    results = cursor.fetchall()
    if str.isdigit(idarg):
        logAction(f"User searched for record in {table} table", f"User input for client's id: {idarg}", "No")
    else:
        logAction(f"User searched for record in {table} table", f"User input for client's id: {idarg}", "Yes")
    return results




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
        
            newInfo = input("Enter the new info ")
            updateInfo(columnName,table,newInfo,uid)
            input("Enter any key to continue\n")

def updateInfo(columnName,table,newInfo,uid):
    sql = f"UPDATE {table} SET {columnName} = ? WHERE id = ?"
    args = (newInfo,uid)
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
            if uid != 'list':
                deleteRecord2(usertype, table, uid)
                
        else:
            deleteRecord2(usertype, table, uid)
            


def listAllUsers():
    print("\n" * 30)
    getColumns('advisors',True)

    print("('SuprAdmID:0', 'Super Admin', 'superadmin' ")
    print("~"*80)
    cursor.execute("SELECT ('AdvisorID:' || id) as id , 'Advisor' as Role, Username FROM advisors")
    advisors = cursor.fetchall()
    for advisor in advisors:
        print(advisor)
    print("~"*80)
    cursor.execute("SELECT ('SystAdmID:' || id) as id , 'System Admin' as Role, Username FROM sysadmins")
    sysadmins = cursor.fetchall()
    for sysadmin in sysadmins:
        print(sysadmin)
    print("="*80)
    logAction("Listed all employees", "", "No")
    input("Enter any key to exit\n")
   

def logAction(dc,ad,sp):
    from currentuser import currentUserName
    username = Encrypt (currentUserName)
    from datetime import date, datetime
    date = Encrypt(str(date.today()))
    time = Encrypt(str((datetime.now()).strftime("%H:%M:%S")))
    desc = Encrypt (dc)
    addinfo = Encrypt (ad)
    sus = Encrypt (sp)

    sql = """INSERT INTO log (Username, Date, Time, Description_of_activity, Additional_information, Suspicious)
                      VALUES (?,?,?,?,?,?)"""
    args = (username,date,time,desc,addinfo,sus)
    cursor.execute(sql,args) 
    connection.commit() 

    if sus == "Yes":
        
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
        for i in row:
            print(Decrypt (i))

    print("="* 100)
    logAction("Displayed logs", "", "No")
    input("\nEnter any key to continue ")


def empty_table():
    name = input("delete content of table. tablename: ")
    cursor.execute("DELETE FROM {}".format(name))
    connection.commit()
    

def drop_table():
    name = input("drop table. tablename: ")
    cursor.execute("DROP TABLE {}".format(name))
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
    while not re.match('^([a-zA-Z\']{1,40})+\ +([a-zA-Z]{1,40})+$', name):
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
    text = str(text)
    shift = 5
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for char in text:
        if char in alpha:
            index = (alpha.find(char) - shift) % len(alpha)
            result += alpha[index]
        else:
            result += char
    return result


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
    