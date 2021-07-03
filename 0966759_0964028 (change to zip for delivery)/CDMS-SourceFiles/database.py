import sqlite3

connection = sqlite3.connect('CDMS.db')
cursor = connection.cursor()


createTableClients = """CREATE TABLE IF NOT EXISTS
clients(id INTEGER PRIMARY KEY AUTOINCREMENT, Full_Name TEXT, Address TEXT, Email_Address TEXT, Mobile_Phone TEXT)"""
cursor.execute(createTableClients)

#create purchase table
createTableLog = """CREATE TABLE IF NOT EXISTS
log(id INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Date TEXT, Description_of_activity TEXT, Additional_information TEXT, Suspicious TEXT)"""
cursor.execute(createTableLog)

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



# cursor.execute("SELECT * FROM clients WHERE Full_Name=:username",{"username":bob})

#injection unprevented
#cursor.execute("SELECT * FROM clients WHERE Full_Name='{}'".format(bob))


def addClientToDb(fn,ad,ea,mp):
    print("adding client to db...")
    sqlargs = (fn,ad,ea,mp)
    sql = "INSERT INTO clients (Full_Name, Address, Email_Address, Mobile_Phone) VALUES (?,?,?,?)"
    cursor.execute(sql,sqlargs)
    connection.commit()
    
    #Sql Injection safe SELECT *


    
#cursor.execute("SELECT * FROM clients WHERE id=:id",{"id":fn})
#cursor.execute("SELECT * FROM clients WHERE Full_Name='{}'".format(fn))
# get results
results = cursor.fetchall()
print(results)