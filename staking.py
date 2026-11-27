# staking feature for crypto wallets
import persistence


# staking yield calculator using recursion (compound interest formula)
def calculate_staking_yield(principal, rate, days):
    if days <= 0:
        return principal
    else:
        next_day_principal = principal * (1 + rate / 100)
        return calculate_staking_yield(next_day_principal, rate, days - 1)


def stake_crypto(userid, cryptocurrency, amount):
    db = persistence.load_db()
    user = db.get(userid)
    if not user or amount <= 0:
        return False

    assets = user["wallet"]["assets"]
    staked = user["wallet"]["staked_assets"]

    source = assets
    destination = staked
    tx_type = "stake"

    if source.get(cryptocurrency, 0) < amount:
        return False

    source[cryptocurrency] -= amount
    destination[cryptocurrency] = destination.get(cryptocurrency, 0) + amount

    persistence.record_transaction(
        user["wallet"]["transactions"], tx_type, amount, "asset", cryptocurrency
    )

    persistence.save_db(db)
    return True


def unstake_crypto(userid, cryptocurrency, amount):
    db = persistence.load_db()
    user = db.get(userid)
    if not user or amount <= 0:
        return False

    assets = user["wallet"]["assets"]
    staked = user["wallet"]["staked_assets"]

    source = staked
    destination = assets
    tx_type = "unstake"

    if source.get(cryptocurrency, 0) < amount:
        return False

    source[cryptocurrency] -= amount
    destination[cryptocurrency] = destination.get(cryptocurrency, 0) + amount

    persistence.record_transaction(
        user["wallet"]["transactions"], tx_type, amount, "asset", cryptocurrency
    )

    persistence.save_db(db)
    return True
