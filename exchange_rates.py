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
    response = requests.get(f"https://v6.exchangerate-api.com/v6/a2b3d026b739a6875092edf5/latest/{base_currency}").json()
    return (
        response.get("conversion_rates")
    )

