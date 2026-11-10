def transfer_funds(senderid, recipientid, amount, currency):
    if amount <= 0:
        return False  # transfer failed due to invalid amount
    if currency not in senderid["balances"]:
        return False  # transfer failed due to invalid currency
    if senderid["balances"][currency] < amount:
        return False  # transfer failed due to insufficient funds

    senderid["balances"][currency] -= amount
    recipientid["balances"][currency] += amount

    return True  # transfer successful