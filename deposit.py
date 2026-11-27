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

    persistence.record_transaction(
        db[accountid]["fiat"]["transactions"], "deposit", amount, "currency", currency
    )

    if currency == "PKR":
        points.reward_points(accountid, amount, db=db)
    persistence.save_db(db)
    return True
