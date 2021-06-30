import sqlite3

connection = sqlite3.connect('testdb.db')
 
cursor = connection.cursor()


command1 = """CREATE TABLE IF NOT EXISTS
stores(store_id INTEGER PRIMARY KEY, location TEXT)"""

cursor.execute(command1)

#create purchase table
command2 = """CREATE TABLE IF NOT EXISTS
purchases(purchase_id INTEGER PRIMARY KEY, store_id INTEGER, total_cost FLOAT,
FOREIGN KEY(store_id) REFERENCES stores(store_id))"""

cursor.execute(command2)

#add to stores
cursor.execute("INSERT INTO stores VALUES(21, 'Afri' )")
cursor.execute("INSERT INTO stores VALUES(22, 'Bafri' )")
cursor.execute("INSERT INTO stores VALUES(23, 'Cafri' )")

#add to purchases
cursor.execute("INSERT INTO purchases VALUES(2, 21, 15 )")
cursor.execute("INSERT INTO purchases VALUES(3, 23, 1.21 )")




cursor.execute("UPDATE purchases SET total_cost = 3.67 WHERE purchase_id = 2")
cursor.execute("DELETE FROM purchases WHERE purchase_id = 3")

cursor.execute("SELECT * FROM purchases")

connection.commit()

# get results
results = cursor.fetchall()
print(results)

