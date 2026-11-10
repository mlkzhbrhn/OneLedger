def withdrawal(accountid, amount, currency):
    # Validate the amount
    if amount <= 0:
        return False  # withdrawal failed due to invalid amount
    if accountid["balances"][currency] < amount:
        return False  # withdrawal failed due to insufficient funds
    if currency not in accountid["balances"]:
        return False  # withdrawal failed due to invalid currency

    accountid["balances"][currency] -= amount  # Deduct the amount from the account balance

    return True  # successful withdrawal