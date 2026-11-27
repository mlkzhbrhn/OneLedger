# conversion functionality for fiat to crypto and vice versa
import exchange_rates
import persistence


def convert_fiat_to_crypto(userid, fiat_amount, fiat_currency, crypto_currency):
    # load db
    db = persistence.load_db()
    # check if user exists in db
    user = db.get(userid)

    if not user:
        return False

    if fiat_amount <= 0:
        return False

    if fiat_amount > user["fiat"]["balances"].get(fiat_currency, 0):
        return False

    exchange_rate = exchange_rates.get_crypto_exchange_rates().get(crypto_currency, 0)

    if exchange_rate == 0:
        return False

    if fiat_currency != "USD":
        fiat_to_usd_rate = exchange_rates.get_fiat_exchange_rates(fiat_currency).get(
            "USD", 0
        )
        if fiat_to_usd_rate == 0:
            return False
        converted_fiat_amount = fiat_amount * fiat_to_usd_rate
        converted_amount = converted_fiat_amount / exchange_rate
    else:
        converted_amount = fiat_amount / exchange_rate

    # update user balances and transactions
    user["fiat"]["balances"][fiat_currency] -= fiat_amount
    user["wallet"]["assets"][crypto_currency] = (
        user["wallet"]["assets"].get(crypto_currency, 0) + converted_amount
    )
    persistence.record_transaction(
        user["fiat"]["transactions"], "sell", fiat_amount, "currency", fiat_currency
    )
    persistence.record_transaction(
        user["wallet"]["transactions"], "buy", converted_amount, "asset", crypto_currency
    )
    persistence.save_db(db)

    return True
