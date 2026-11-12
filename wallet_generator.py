import hashlib
import random

def generate_wallet(seed_phrase):
    wallet_address = "0x" + hashlib.sha256(seed_phrase.encode('utf-8')).hexdigest()[:40]
    return wallet_address

def generate_seed_phrase():
    word_list = [
        "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yellowfruit", "zucchini"
        ]
    seed_phrase = ""
    for _ in range(12):
        seed_phrase += random.choice(word_list) + " "
        
    return seed_phrase.strip()

seed = generate_seed_phrase()
address = generate_wallet(seed)
