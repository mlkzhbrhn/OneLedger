def transfer_funds(senderid, recipientid, amount):
    if amount <= 0:
        return "Transfer amount must be greater than zero."
    
    if senderid.balance < amount:
        return "Insufficient funds in sender's account."
    
    senderid.balance -= amount
    recipientid.balance += amount
    
    return ("Successfully transferred " + str(amount) + " from " + senderid.name + " to " + recipientid.name + ".")