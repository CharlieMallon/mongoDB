import os
import pymongo

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


def find_record():
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


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            print("you have selected option 2")
        elif option == "3":
            print("you have selected option 3")
        elif option == "4":
            print("you have selected option 4")
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")

conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()