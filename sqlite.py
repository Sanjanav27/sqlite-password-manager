import sqlite3

conn=sqlite3.connect('test.db')

print("Opened database successfully")

conn.execute('CREATE TABLE credential (detail TEXT, cred TEXT)')
#conn.execute("select * from credential")

print("Table created successfully")
conn.close()

