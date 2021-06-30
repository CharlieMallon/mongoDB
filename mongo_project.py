import os
import pymongo
from pymongo.message import delete

# importing environment variables, if env.py exists
if os.path.exists("env.py"):
    import env

# setting constant variables
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConectionFailure as e:
        print("Could not connect to MongoDB: %s") % e

def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record():
    print("")
    first = input("enter first name >")
    last = input("enter last name >")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found")
    
    return doc

def add_record():
    print("")
    first = input("enter first name >")
    last = input("enter last name >")
    dob = input("enter date of birth>")
    gender = input("enter gender >")
    hair_color = input("enter hair color >")
    occupation = input("enter occupation >")
    nationality = input("enter nationality >")

    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_color": hair_color,
        "occupation": occupation,
        "nationality": nationality
    }

    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    if doc:
        print("")
        # k = key, v = values
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        # k = key, v = values
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v.capitalize() + "] > ")
                
                if update_doc[k] == "":
                    update_doc[k] = v
        
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
        
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")

        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document Deleted!")
            except:
                print("Error accessing the data")
        else:
            print("")
            print("Document not deleted")
        



def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")

conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()