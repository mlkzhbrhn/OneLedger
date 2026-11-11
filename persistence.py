import json # importing json since python dictionaries are same as json objects, so we can use json to read and write to the db.json file

db_file = "db.json" # path to the database file

# function to load the database from the db.json file
def load_db():
    with open(db_file, "r") as f:
        return json.load(f) # loading and returning the database from the db.json file as a python dictionary

def save_db(db):
    with open(db_file, "w") as f:
        json.dump(db, f, indent=2) # saving the database to the db.json file as a json object with indentation for readability