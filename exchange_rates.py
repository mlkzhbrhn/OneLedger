import requests
def get_exchange_rates():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd").json()
    # print(response)
    return {
        "BTC": response.get("bitcoin", {}).get("usd", 0),
        "ETH": response.get("ethereum", {}).get("usd", 0),
        "SOL": response.get("solana", {}).get("usd", 0)
    }
