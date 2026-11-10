def deposit(accountid, amount, currency):
    if amount <= 0:
        return False  # deposit failed due to invalid amount
    
    if not currency or not isinstance(currency, str):
        return False  # deposit failed due to invalid currency
    
    accountid["balance"][currency] = accountid["balance"].get(currency, 0) + amount  # Add the amount to the account balance
    
    return True # successful deposit