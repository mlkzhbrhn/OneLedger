# reward users with points for their transactions (send-only PKR transactions)
# earn: 1 point = 100 PKR
# redeem: 1 point = 1 PKR
import persistence

MIN_TRANSACTION_AMOUNT = 100
MIN_REDEEM_POINTS = 10
PKR_PER_POINT = 1


def reward_points(username, amount, db=None):
    if amount < MIN_TRANSACTION_AMOUNT:
        return False

    owns_db = db is None
    if owns_db:
        db = persistence.load_db()

    if username not in db:
        return False

    points_earned = int(amount // MIN_TRANSACTION_AMOUNT)

    db[username]["points"] += points_earned

    persistence.record_transaction(
        db[username]["fiat"]["transactions"],
        "points reward",
        points_earned,
        "currency",
        "points",
    )
    if owns_db:
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

    persistence.record_transaction(
        db[username]["fiat"]["transactions"],
        "points redemption",
        pkr_value,
        "currency",
        "PKR",
    )

    persistence.save_db(db)
    return True
