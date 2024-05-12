import mysql.connector

#1. Create Connection

db =  mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '12345',
    database = 'wbs_januar'
    
)

#2. Create Cursor

mycursor = db.cursor()

#3. Define SQL Statement

sql_statement = 'SELECT p_id FROM person2 Order by p_id desc;'


#4. Execute SQL Statement

mycursor.execute(sql_statement) # mycursor.execute('SHOW TABLES;')

#5. Display Data

for row in mycursor:
    print(row)

#6. Close the connection
db.close