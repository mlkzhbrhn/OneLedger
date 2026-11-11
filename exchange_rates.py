import requests
def get_crypto_exchange_rates():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd").json()
    # print(response)
    return {
        "BTC": response.get("bitcoin", {}).get("usd", 0),
        "ETH": response.get("ethereum", {}).get("usd", 0),
        "SOL": response.get("solana", {}).get("usd", 0)
    }
def get_fiat_exchange_rates(base_currency):
    import config
    EXCHANGE_RATE_API_KEY = config.EXCHANGE_RATE_API_KEY
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}").json()
    return (
        response.get("conversion_rates")
    )

