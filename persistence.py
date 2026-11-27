import datetime
import json  # importing json since python dictionaries are same as json objects, so we can use json to read and write to the db.json file

import config

db_file = config.DB_FILE  # path to the database file


# function to load the database from the db.json file
def load_db():
    with open(db_file, "r") as f:
        return json.load(
            f
        )  # loading and returning the database from the db.json file as a python dictionary


def save_db(db):
    with open(db_file, "w") as f:
        json.dump(
            db, f, indent=2
        )  # saving the database to the db.json file as a json object with indentation for readability


def record_transaction(transactions, tx_type, amount, unit_key, unit_value):
    transactions.append(
        {
            "id": len(transactions) + 1,
            "type": tx_type,
            "amount": amount,
            unit_key: unit_value,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    )
