def withdrawal(accountid, amount):
    # Validate the amount
    if amount <= 0:
        return False  # withdrawal failed due to invalid amount
    
    accountid["balance"] -= amount  # Deduct the amount from the account balance
    
    return True # successful withdrawal