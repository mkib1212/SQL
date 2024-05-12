import os
import sqlite3
from pathlib import Path
import json

def open_json():
    with open ("./menu2023-2.json", mode = 'r', encoding = "UTF-8") as file:
       menu = json.load(file)
    return menu
    
def connection_cursor():
    
    DB_FILE_PATH = Path(__file__).parent / 'acasa1.db'


    #1. create connection
    db = sqlite3.connect(DB_FILE_PATH, timeout = 10)


    #2. create cursor
    mycursor = db.cursor()
    
    return mycursor, db



def insert_menu_into_db(menu,db,mycursor):
    #get the categories from the menu
    data= [] #category list
    
    for category in menu.keys():
        data.append((category,))
        
    for category in data:
        sql = "INSERT INTO category (category_title) VALUES (?);"   
        with db: #without using commit 
            
            #insert the category name and get the primary key
            mycursor.execute(sql, category)
            
            dishes = []
            
            for dish in menu[category[0]]:
                #built the tuple for each dish
                dish_data = (dish["id"], dish["title"],  mycursor.lastrowid, dish["price"])
                
                # add the dish to a list of dishes
                dishes.append(dish_data)
            
            #insert the dishes into menu table
            sql = "INSERT INTO menu (id, title, FK_id_category, price) VALUES (?,?,?,?);"
            mycursor. executemany(sql, dishes)
        





   
def commit_close_db(db):
         
    # commit the changes
    db.commit()

    # Close connection
    db.close()
    
def main():
    menu = open_json()
    mycursor, db = connection_cursor()
    insert_menu_into_db(menu,db,mycursor)
    commit_close_db(db)
    
main()