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
log(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT, Suspicious TEXT)"""
cursor.execute(createTableLog)

createTableUnreadSuspicous = """CREATE TABLE IF NOT EXISTS
unreadsuslogs(susID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Time TEXT, Description_of_activity TEXT, Additional_information TEXT)"""
cursor.execute(createTableUnreadSuspicous)

connection.commit()
#=========================================================================================================   Register  =====================================

cities = ["Rotterdam", "Amsterdam", "Den Haag", "Eindhoven","Maastricht","Delft","Breda","Haarlem","Utrecht","Leiden"]


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
        logAction("Client has been added to the database", f"Inputs: {sqlargs}", "No")

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
    print("Client '{}' has been added to the database".format(name))
    input("Enter any key to continue\n")


def registerAdvisor():
    def addAdvisorToDb(un,pw,fn,ln,dt):
        sqlargs = (un,pw,fn,ln,dt)
        sql = "INSERT INTO advisors (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction("Advisor has been added to the database", f"Inputs: {sqlargs}", "No")

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
    print("\n"+ "="*40)
    print("Advisor '" + uname + "' has been registered on " + date)
    input("Enter any key to continue\n")




def registerSystemAdmin():
    def addSystemAdminToDb(un,pw,fn,ln,dt):
        sqlargs = (un,pw,fn,ln,dt)
        sql = "INSERT INTO sysadmins (Username, Password, First_Name, Last_Name, Registered_Date) VALUES (?,?,?,?,?)"
        cursor.execute(sql,sqlargs)
        connection.commit()
        logAction("System admin has been added to the database", f"Inputs: {sqlargs}", "No")
   
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
    print("\nSystem admin " + uname + " has been registered on " + date)
    input("Enter any key to continue ")


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
        
        choicedesc = "Enter the id of suspicious activity to mark it as read\nOR\nEnter'x' to exit\n\n"
        choice = input(choicedesc)
        if choice != 'x':
            cursor.execute(f"DELETE FROM unreadsuslogs WHERE susID=:id",{"id":choice})
            connection.commit()
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

            columnName = input("Enter the name of the column that you want to modify: ")
            newInfo = input("Enter the new info ")
            updateInfo(columnName,table,newInfo,uid)
            input("Enter any key to continue\n")

def updateInfo(columnName,table,newInfo,uid):
    sql = f"UPDATE {table} SET {columnName} = ? WHERE id = ?"
    args = (newInfo,uid)
    cursor.execute(sql,args)
    connection.commit()
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
        else:
            cursor.execute(f"DELETE FROM {table} WHERE id=:id",{"id":uid})
            connection.commit()
            print("\n" * 40)
            print(f"{uid} '{info[0][1]}' with id:{info[0][0]} has been deleted\n")
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
    input("Enter any key to exit\n")
   

def logAction(dc,ad,sp):
    from currentuser import currentUserName
    username = currentUserName
    from datetime import date, datetime
    date = str(date.today())
    time = str((datetime.now()).strftime("%H:%M:%S"))
    desc = dc
    addinfo = ad
    sus = sp

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
        print(row)
    print("="* 100)
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

