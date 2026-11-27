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

    persistence.record_transaction(
        db[accountid]["fiat"]["transactions"],
        "withdrawal",
        amount,
        "currency",
        currency,
    )

    persistence.save_db(db)
    return True
