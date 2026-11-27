import persistence


def deposit_to_savings(username, amount, currency):
    if amount <= 0 or not currency or not isinstance(currency, str):
        return False

    currency = currency.upper()
    db = persistence.load_db()

    if username not in db:
        return False

    fiat = db[username]["fiat"]
    balances = fiat["balances"]
    savings = fiat["savings"]

    source = balances
    destination = savings
    tx_type = "savings_deposit"

    if currency not in source or source[currency] < amount:
        return False

    source[currency] -= amount
    destination[currency] = destination.get(currency, 0) + amount

    persistence.record_transaction(
        fiat["transactions"], tx_type, amount, "currency", currency
    )
    persistence.save_db(db)
    return True


def withdraw_from_savings(username, amount, currency):
    if amount <= 0 or not currency or not isinstance(currency, str):
        return False

    currency = currency.upper()
    db = persistence.load_db()

    if username not in db:
        return False

    fiat = db[username]["fiat"]
    balances = fiat["balances"]
    savings = fiat["savings"]

    source = savings
    destination = balances
    tx_type = "savings_withdrawal"

    if currency not in source or source[currency] < amount:
        return False

    source[currency] -= amount
    destination[currency] = destination.get(currency, 0) + amount

    persistence.record_transaction(
        fiat["transactions"], tx_type, amount, "currency", currency
    )
    persistence.save_db(db)
    return True

