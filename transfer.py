def transfer_funds(senderid, recipientid, amount):
    if amount <= 0:
        return False  # transfer failed due to invalid amount
    if senderid["balance"] < amount:
        return False  # transfer failed due to insufficient funds

    senderid["balance"] -= amount
    recipientid["balance"] += amount
    
    return True  # transfer successful