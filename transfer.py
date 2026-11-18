import datetime
import persistence

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

    sender_txs = db[senderid]["fiat"]["transactions"]
    sender_txs.append({
        "id": len(sender_txs) + 1,
        "type": "transfer_out",
        "amount": amount,
        "currency": currency,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    })

    recipient_txs = db[recipientid]["fiat"]["transactions"]
    recipient_txs.append({
        "id": len(recipient_txs) + 1,
        "type": "transfer_in",
        "amount": amount,
        "currency": currency,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    })

    persistence.save_db(db)
    return True