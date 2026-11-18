import datetime
import persistence

def withdrawal(accountid, amount, currency):
    if amount <= 0 or not currency or not isinstance(currency, str):
        return False

    currency = currency.upper()
    db = persistence.load_db()

    if accountid not in db:
        return False

    balances = db[accountid]["fiat"]["balances"]
    if currency not in balances or balances[currency] < amount:
        return False

    balances[currency] -= amount

    transactions = db[accountid]["fiat"]["transactions"]
    transactions.append({
        "id": len(transactions) + 1,
        "type": "withdrawal",
        "amount": amount,
        "currency": currency,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    })

    persistence.save_db(db)
    return True