wallet_db = {
    "user1": {
        "seed": "apple banana cherry date elderberry fig grape honeydew kiwi lemon mango nectarine",
        "address": "0x1234567890abcdef1234567890abcdef12345678",
        "assets": { "BTC": 1.5, "ETH": 10.0, "USDT": 1000.0 },
        "staked_assets": { "BTC": 0.5, "ETH": 2.0 }
    }
}

import requests
def get_exchange_rates():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd").json()
    # print(response)
    return {
        "BTC": response.get("bitcoin", {}).get("usd", 0),
        "ETH": response.get("ethereum", {}).get("usd", 0),
        "SOL": response.get("solana", {}).get("usd", 0)
    }
