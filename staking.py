# staking feature for crypto wallets
import persistence
import datetime

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
    if user["wallet"]["assets"].get(cryptocurrency, 0) < amount:
        return False

    current_staked = user["wallet"]["staked_assets"].get(cryptocurrency, 0)

    # update balances
    user["wallet"]["assets"][cryptocurrency] -= amount
    user["wallet"]["staked_assets"][cryptocurrency] = current_staked + amount

    # record transaction
    transaction ={
        "id": len(user["wallet"]["transactions"]) + 1,
        "type": "stake",
        "amount": amount,
        "asset": cryptocurrency,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    user["wallet"]["transactions"].append(transaction)

    persistence.save_db(db)
    return True