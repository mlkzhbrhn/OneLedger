import persistence
import points


def transfer_funds(senderid, recipientid, amount, currency):
    if amount <= 0 or not currency or not isinstance(currency, str):
        return False
    if senderid == recipientid:
        return False

    currency = currency.upper()
    db = persistence.load_db()

    if senderid not in db or recipientid not in db:
        return False

    sender_balances = db[senderid]["fiat"]["balances"]
    if currency not in sender_balances or sender_balances[currency] < amount:
        return False

    recipient_balances = db[recipientid]["fiat"]["balances"]

    sender_balances[currency] -= amount
    recipient_balances[currency] = recipient_balances.get(currency, 0) + amount

    persistence.record_transaction(
        db[senderid]["fiat"]["transactions"],
        "transfer_out",
        amount,
        "currency",
        currency,
    )
    persistence.record_transaction(
        db[recipientid]["fiat"]["transactions"],
        "transfer_in",
        amount,
        "currency",
        currency,
    )

    if currency == "PKR":
        points.reward_points(senderid, amount, db=db)
    persistence.save_db(db)
    return True
