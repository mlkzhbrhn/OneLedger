# user authentication
import persistence
import wallet_generator
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, password, role):
    db = persistence.load_db()
    if username in db:
        return False # user already exists

    if len(username) < 3 or len(username) > 20:
        return False 
    if len(password) < 8:
        return False
    seed = wallet_generator.generate_seed_phrase()

    db[username] = {
    "role": role,
    "password": hash_password(password),

    "points": 0,
    "loans": [],

    "fiat": {
    "balances": {"PKR": 0, "USD": 0},
    "transactions": []
    },

    "wallet": {
        "address": wallet_generator.generate_wallet(seed),
        "assets": {"BTC": 0, "ETH": 0, "SOL": 0},
        "staked_assets": {"BTC": 0, "ETH": 0, "SOL": 0},
        "transactions": []
    }
    }
    persistence.save_db(db)

    return True


def login_user(username, password):
    db = persistence.load_db()
    if username not in db:
        return False
    password_hash = hash_password(password)

    if db[username]["password"] != password_hash:
        return False

    return True