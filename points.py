# reward users with points for their transactions (send-only PKR transactions)
# earn: 1 point = 100 PKR
# redeem: 1 point = 1 PKR
import datetime

import persistence

MIN_TRANSACTION_AMOUNT = 100
MIN_REDEEM_POINTS = 10
PKR_PER_POINT = 1


def reward_points(username, amount):
    if amount < MIN_TRANSACTION_AMOUNT:
        return False

    db = persistence.load_db()

    if username not in db:
        return False

    points_earned = int(amount // MIN_TRANSACTION_AMOUNT)

    db[username]["points"] += points_earned

    db[username]["fiat"]["transactions"].append(
        {
            "id": len(db[username]["fiat"]["transactions"]) + 1,
            "type": "points reward",
            "amount": points_earned,
            "currency": "points",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    )
    persistence.save_db(db)
    return True


def redeem_points(username, points):
    if points < MIN_REDEEM_POINTS:
        return False

    db = persistence.load_db()

    if username not in db:
        return False

    if db[username]["points"] < points:
        return False

    pkr_value = points * PKR_PER_POINT
    db[username]["points"] -= points
    db[username]["fiat"]["balances"]["PKR"] += pkr_value

    db[username]["fiat"]["transactions"].append(
        {
            "id": len(db[username]["fiat"]["transactions"]) + 1,
            "type": "points redemption",
            "amount": pkr_value,
            "currency": "PKR",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    )

    persistence.save_db(db)
    return True
