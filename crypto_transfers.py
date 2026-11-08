def send_crypto(sender, receiver, asset, amount, gas_fee):
    # checks for sufficient balance and gas fee
    if asset == "ETH":
        if sender["assets"].get("ETH", 0) < (amount + gas_fee):
            return "Insufficient ETH balance for transfer and gas fee"
        
    if sender["assets"].get("ETH", 0) < gas_fee:
        return "Insufficient ETH for gas fee"
    
    if sender["assets"].get(asset, 0) < (amount):
        return f"Insufficient {asset} balance for transfer"
    
    # deduct the amount and gas fee from sender's balance
    sender["assets"][asset] -= (amount)
    sender["assets"]["ETH"] -= gas_fee
    
    # Add the amount to receiver's balance
    receiver["assets"][asset] = receiver["assets"].get(asset, 0) + amount
    
    return "Transfer successful"