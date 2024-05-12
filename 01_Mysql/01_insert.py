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
##1.Variante
sql_statement = 'INSERT INTO kurs2 VALUES (79,"Spanisch"),(99,"AAA");'

##2. Variante
id = 292
title = 'Türkisch'
sql_statement1 = f' INSERT INTO kurs2 VALUES ({id}, "{title}");' 

##3. Variante
sql_statement2 = 'INSERT INTO kurs2 VALUES (%s,%s);'
data123 = (192, 'japanisch')

#4. Execute SQL Statement

mycursor.execute(sql_statement)
mycursor.execute(sql_statement1)
mycursor.execute(sql_statement2,data123)



#5. commit the changes
db.commit()

#6. Display Data
mycursor.execute('SELECT * FROM kurs2;')
for row in mycursor:
    print(row)
    
#6. Close the connection
db.close 
print('saves successfully')