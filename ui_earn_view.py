import flet as ft

import persistence
from ui_helpers import asset_card


def earn_screen(page, username):
    db = persistence.load_db()
    user = db[username]
    staked_assets = user["wallet"].get("staked_assets", {})
    fiat_savings = user["fiat"].get("savings", {})

    btc_staked = staked_assets.get("BTC", 0)
    eth_staked = staked_assets.get("ETH", 0)
    sol_staked = staked_assets.get("SOL", 0)

    pkr_savings = fiat_savings.get("PKR", 0)
    usd_savings = fiat_savings.get("USD", 0)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Staked Crypto", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        asset_card(
                            "BTC",
                            btc_staked,
                            "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
                        ),
                        asset_card(
                            "ETH",
                            eth_staked,
                            "https://cryptologos.cc/logos/ethereum-eth-logo.png",
                        ),
                        asset_card(
                            "SOL",
                            sol_staked,
                            "https://cryptologos.cc/logos/solana-sol-logo.png",
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        ft.Text("Fiat Savings", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Coming soon", size=12, color=ft.Colors.GREY),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        asset_card(
                            "PKR", pkr_savings, "https://flagcdn.com/w80/pk.png"
                        ),
                        asset_card(
                            "USD", usd_savings, "https://flagcdn.com/w80/us.png"
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=10,
        expand=True,
    )
