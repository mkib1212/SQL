#install in the terminal: pip install mymongo

from pymongo import MongoClient

# #1. Create a cluster
# server = MongoClient('mongodb://localhost:27017')
# #2. Create DB object and collection
# my_data_base = server['WBS1']
# collection = my_data_base['mitarbeiter']


db_name = "wbs1"
collection_name = "mitarbeiter"

#1. Create a cluster
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)

#2. Create DB object and collection

db = client[db_name]
collection = db[collection_name]

#3. insert
#CRUD

#insert Document
################

#collection.insert_one({'_id':1})
#collection.insert_one({"vorname": "Manuella"})
#collection.insert_one({"vorname": "alex", "name": "WWWW", "age":20})

#function insert one record
##################
def insert_one_record():
    data = {'_id':5, "ort": "Bremen"}
    collection.insert_one(data)
    

# insert many records
#########################
data1 = [{'stadt': 'Hannover'}, {'stadt': 'Berlin', 'plz': 30000}]
data2 = [{'_id':60, 'vorname':'Johnny'}]
datas = data1 + data2
#collection.insert_many([{'stadt': 'Hamburg'}, {'stadt': 'Bremen', 'plz': 28199}, {'_id':50, 'vorname':'John'}])
#collection.insert_many(datas)

# function insert many records
##############################
def insert_many_records():
    data1 = [{'stadt': 'Hannover1'}, {'stadt': 'Berlin1', 'plz': 40000}]
    data2 = [{'_id':70, 'vorname':'Bill'}]
    datas = data1 + data2
    collection.insert_many(datas)


def main():
    #insert_one_record()
    #insert_many_records()
    pass
    
if __name__ == "__main__":
    main()

# #search one record
#######################
# result = collection.find_one({'age': 20})
# print(result)

#search many record
###################
result = collection.find({'ort': 'Bremen'})
print(result)
for doc in result: # gives the dictionaries
    print(doc)

#update
########
#collection.update_one({'_id':1},{'$set':{'telnr':1234, 'nachname': 'neuer nachname'}})
# old_data = {'_id':1}
# new_data = {'set':{'telnr':12342, 'nachname': 'neuer nachname2'}}
# collection.update_one(old_data,{'$set':new_data})
    
#collection.delete_one ({'age': 20})
#collection.delete_many({'ort': 'Bremen'})

#count documnets in a collection
################
data_count = collection.count_documents({})
print(data_count)