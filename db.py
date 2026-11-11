db = {
    "user1": {
        "role": "admin",
        "password": "********",

        "points": 1000,
        "loans": [{"amount": 500, "interest_rate": 0.05, "due_date": "2023-12-31"}],

        "fiat": {
        "balances": {"PKR": 1000, "USD": 500},
        "transactions": [{"id": 1, "type": "deposit", "amount": 1000, "currency": "PKR", "date": "2023-01-01"}],
        },

        "wallet": {
            "address": "0x...",
            "assets": {"BTC": 0.1, "ETH": 5},
            "staked_assets": {"BTC": 0.05, "ETH": 2.5},
            "transactions": [{"id": 1, "type": "transfer", "amount": 0.1, "asset": "BTC", "date": "2023-01-01"}],
        }
    }
}
