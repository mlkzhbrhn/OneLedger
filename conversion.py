import exchange_rates
import persistence


def convert_fiat_to_crypto(userid, fiat_amount, fiat_currency, crypto_currency):
    db = persistence.load_db()
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


def convert_crypto_to_fiat(userid, crypto_amount, crypto_currency, fiat_currency):
    db = persistence.load_db()
    user = db.get(userid)

    if not user or crypto_amount <= 0:
        return False

    if crypto_amount > user["wallet"]["assets"].get(crypto_currency, 0):
        return False

    crypto_usd_rate = exchange_rates.get_crypto_exchange_rates().get(
        crypto_currency, 0
    )
    if crypto_usd_rate == 0:
        return False

    usd_amount = crypto_amount * crypto_usd_rate

    if fiat_currency != "USD":
        usd_to_fiat_rate = exchange_rates.get_fiat_exchange_rates("USD").get(
            fiat_currency, 0
        )
        if usd_to_fiat_rate == 0:
            return False
        converted_fiat_amount = usd_amount * usd_to_fiat_rate
    else:
        converted_fiat_amount = usd_amount

    user["wallet"]["assets"][crypto_currency] -= crypto_amount
    user["fiat"]["balances"][fiat_currency] = (
        user["fiat"]["balances"].get(fiat_currency, 0) + converted_fiat_amount
    )
    persistence.record_transaction(
        user["wallet"]["transactions"],
        "sell",
        crypto_amount,
        "asset",
        crypto_currency,
    )
    persistence.record_transaction(
        user["fiat"]["transactions"],
        "buy",
        converted_fiat_amount,
        "currency",
        fiat_currency,
    )
    persistence.save_db(db)

    return True
