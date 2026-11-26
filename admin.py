import persistence


# get liquidity for entire system
def get_liquidity():
    db = persistence.load_db()

    fiat_totals = {}
    crypto_totals = {}
    staked_crypto_totals = {}

    for user in db.values():
        fiat_data = user["fiat"]
        for currency, balance in fiat_data["balances"].items():
            fiat_totals[currency] = fiat_totals.get(currency, 0) + balance

        crypto_data = user["wallet"]
        for currency, balance in crypto_data["assets"].items():
            crypto_totals[currency] = crypto_totals.get(currency, 0) + balance

        for currency, balance in crypto_data["staked_assets"].items():
            staked_crypto_totals[currency] = (
                staked_crypto_totals.get(currency, 0) + balance
            )

    return {
        "fiat_totals": fiat_totals,
        "crypto_totals": crypto_totals,
        "staked_crypto_totals": staked_crypto_totals,
    }


# get transaction history for entire system
def get_transaction_history():
    db = persistence.load_db()
    transaction_history = []  # merged based on date

    for username, data in db.items():
        fiat_transactions = data["fiat"].get("transactions", [])
        crypto_transactions = data["wallet"].get("transactions", [])

        for transaction in fiat_transactions:
            transaction_history.append(
                {
                    **transaction,
                    "username": username,
                    "currency": transaction.get("currency", ""),
                }
            )  # unpack transaction dict and add username
        for transaction in crypto_transactions:
            transaction_history.append(
                {
                    **transaction,
                    "username": username,
                    "currency": transaction.get("asset", ""),
                }
            )  # normalize currency field for fiat and crypto transactions

    return sorted(
        transaction_history, key=lambda x: x["date"], reverse=True
    )  # sort by date, most recent first


def get_user_data(username=None):
    db = persistence.load_db()

    if username is None:
        return sanitise_user_data(db)
    else:
        if username in db:
            return sanitise_user_data({username: db[username]})
        else:
            return {}  # user not found


def sanitise_user_data(user_data):
    sanitised_data = {}
    for username, data in user_data.items():
        sanitised_data[username] = {}
        for key, value in data.items():
            if key != "password":
                sanitised_data[username][key] = value
    return sanitised_data
