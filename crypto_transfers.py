import persistence


def send_crypto(sender, receiver, asset, amount, gas_fee=0.01):
    if sender == receiver:
        return False  # cannot send to self

    if amount <= 0 or gas_fee < 0:
        return False  # cannot send non-positive amount or negative gas fee

    db = persistence.load_db()

    # fetch sender and receiver's data
    sender_data = db.get(sender)
    receiver_data = db.get(receiver)

    if not sender_data or not receiver_data:
        return False  # either sender or receiver does not exist

    # fetch sender and receiver's wallet data
    sender_wallet = sender_data["wallet"]
    receiver_wallet = receiver_data["wallet"]

    # fetch sender and receiver's assets
    sender_assets = sender_wallet["assets"]
    receiver_assets = receiver_wallet["assets"]

    # checks for sufficient balance and gas fee
    if asset == "ETH":
        if sender_assets.get("ETH", 0) < (amount + gas_fee):
            return False  # insufficient ETH balance for transfer and gas fee

    if sender_assets.get("ETH", 0) < gas_fee:
        return False  # insufficient ETH balance for gas fee

    if sender_assets.get(asset, 0) < (amount):
        return False  # insufficient balance for transfer

    # deduct the amount and gas fee from sender's balance
    sender_assets[asset] -= amount
    sender_assets["ETH"] -= gas_fee

    # Add the amount to receiver's balance
    receiver_assets[asset] = receiver_assets.get(asset, 0) + amount

    persistence.record_transaction(
        sender_wallet["transactions"], "transfer_out", amount, "asset", asset
    )
    persistence.record_transaction(
        receiver_wallet["transactions"], "transfer_in", amount, "asset", asset
    )

    persistence.save_db(db)

    return True
