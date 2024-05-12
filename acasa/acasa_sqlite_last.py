import os
import sqlite3
from pathlib import Path


def connection_cursor():

    DB_FILE_PATH = Path(__file__).parent /'acasa1.db'

    #1. create connection
    db = sqlite3.connect(DB_FILE_PATH)


    #2. create cursor
    mycursor = db.cursor()
    
    return mycursor, db






#ask for customer data
def customer_data(mycursor,db):
    name = input('Enter your name: ')
    surname = input('Enter your surname: ')
    plz = input('Enter your postal code: ')
    
    mycursor.execute('SELECT * from customers;')
    customers =  mycursor.fetchall()
    cust_name_plz = [[data[1], data[2], data[3]] for data in customers]  #[[name, surname, plz], ...]
    
    customer_ids = [id[0] for id in customers] #list of customer ids
    
    
    exist_cus_index =  [i for i, x in enumerate(cust_name_plz) if x == [name, surname, plz]] #   the index (in a list) if customer already exists
    
    if bool(exist_cus_index): # if exist_cus_index is not empty, customer exists
       last_customer_id = customer_ids[exist_cus_index[0]] 
       
        
        
    else:    #  if customer does not exist
        
        with db:
            mycursor.execute('INSERT INTO customers (name, surname, plz) VALUES ( ?, ?, ? ) ;', [name, surname, plz] ) #insert data into customers table
            
       
            mycursor.execute('SELECT id_customer FROM customers;')
            customer_ids = mycursor.fetchall()
            customer_ids = [id[0] for id in customer_ids] #updated list of customer id
        last_customer_id = customer_ids[-1] # last customer id, if new customer



    
    return last_customer_id, customer_ids

def invoice_id(mycursor):
    mycursor.execute('INSERT INTO invoice (rechnung_id) VALUES (NULL); ',)
    mycursor.execute('SELECT * FROM invoice;')
    invoice_nr = mycursor.fetchall()
    invoice_nr = [id[0] for id in invoice_nr] #list of invoice numbers, column rechnung_i
    last_invoice_nr = invoice_nr[-1]
   
   
    return last_invoice_nr


def print_header():

    print("Willkommen bei ACASA")
    print(20*'-')

#show menu
def show_menu(mycursor):
    
    mycursor.execute('SELECT * FROM category;')
    category = mycursor.fetchall() #[(id_category, category_title), ..]
    
    mycursor.execute('SELECT * FROM menu ;')
    menu_table = mycursor.fetchall()
    
    for i in range(len(category)):
        mycursor.execute('SELECT category_title  FROM category WHERE id_category =  ? ;', (category[i][0],)) # get  category names through category ids
        print(f"\n{category[i][1]}\n{20*'*'}")
        for j in range(len(menu_table)):    
           if  menu_table[j][2] == category[i][0]:   # finds the dishes with category id = fk_category_id
              print(f"{menu_table[j][0]}. {menu_table[j][1]}\t{menu_table[j][3]} Euro") # print rows of the table menu where category_id  =  fk_category_id
    
    
        
    
    ids_menu = [id[0] for id in menu_table] # list of ids in table menu
    
    
    return ids_menu, menu_table


# # Get user wishes

def user_wish(mycursor, ids_menu:list, last_customer_id,last_invoice_nr):
    user_wish_list = []
    while True:
        
        user_wish = int(input("Was möchten Sie bestellen: "))
        
        if user_wish in ids_menu:
            mycursor.execute('INSERT INTO orders (FK_id_customer, FK_id_menu, fk_rechnung_id ) VALUES ( ?, ?, ?);', [last_customer_id, user_wish, last_invoice_nr])
        
        # exit point
        if user_wish == 0:
            break # exit the loop

        if user_wish not in ids_menu:
            print(f"{user_wish} bieten wir leider nicht an")
            continue # jump to the header of the loop, to the next iteration

        user_wish_list.append(user_wish)

    # Sort the Wish IDs
    user_wish_list.sort()
    
    return user_wish_list
    


# Quittung

def print_quittung(mycursor, user_wish_list, menu_table,last_customer_id, customer_ids:list, last_invoice_nr):
    message1 = "Quittung\n"
    message1 += "*" * 10 + "\n"

    customer_last = mycursor.execute('SELECT * from customers;')
    customer_last = mycursor.fetchall()[customer_ids.index(last_customer_id)] # customer data of last customer, index
    customer_last = f'customer: {customer_last[0]}. {customer_last[1]} {customer_last[2]}, {customer_last[3]}' #last customer's name, address and plz from the customer table
    
    message1 += f"Invoice {last_invoice_nr}\n"

    message1 += f"{customer_last} \n{30 * '-'}\n"
    

    id_list = [[id[0]] for id in menu_table] # [[100], [101], [102], [200], [201], [202], [300], [301], [400], [401], [402]] for iteration 
    join_menu_category = mycursor.execute('SELECT category_title, title, price FROM menu LEFT JOIN category ON fk_id_category = id_category;')
    join_menu_category = mycursor.fetchall()

    total = 0
    message = ''
    for wish_id in user_wish_list: # [100,200,..]
        for i in range(len(menu_table)):
            for id  in id_list[i]:
               if id == wish_id: # found the dish with the same id
                 message += f'{id}. {join_menu_category[i][0]} {join_menu_category[i][1]}\t{join_menu_category[i][2]}€\n'
                 total += join_menu_category[i][2]


   
    message += "*" * 20 + "\n"
    message += f"Gesamt: {total} €\n"
    message += "*" * 20 + "\n"
    message += "Vielen Dank für Ihren Besuch !\n"
    print(message1)
    print(message)
    return message1, message
    


    

# Save the Receipt to text file
def save_to_txt(message1, message):
    with open("./receipt.txt", mode = "w", encoding= "UTF-8") as file:
        file.write(message1)
        file.write(message)
   
def commit_close_db(db):
         
    # commit the changes
    db.commit()

    # Close connection
    db.close()
    
def main():
    mycursor, db = connection_cursor()
    last_customer_id, customer_ids = customer_data(mycursor, db)
    last_invoice_nr = invoice_id(mycursor)
    print_header()
    ids_menu, menu_table = show_menu(mycursor)
    user_wish_list = user_wish(mycursor, ids_menu, last_customer_id, last_invoice_nr)
    message1, message = print_quittung(mycursor, user_wish_list, menu_table,last_customer_id, customer_ids, last_invoice_nr)
    save_to_txt(message1, message)
    commit_close_db(db)
    
main()