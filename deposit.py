import datetime
import persistence
import points

def deposit(accountid, amount, currency):
    if amount <= 0 or not currency or not isinstance(currency, str):
        return False

    currency = currency.upper()
    db = persistence.load_db()

    if accountid not in db:
        return False

    balances = db[accountid]["fiat"]["balances"]
    balances[currency] = balances.get(currency, 0) + amount

    transactions = db[accountid]["fiat"]["transactions"]
    transactions.append({
        "id": len(transactions) + 1,
        "type": "deposit",
        "amount": amount,
        "currency": currency,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    })

    points.reward_points(accountid, amount)
    persistence.save_db(db)
    return True