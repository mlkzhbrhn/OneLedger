import flet as ft

import command_executor
import crypto_transfers
import persistence
import staking
from ui_helpers import asset_card, go_back


def send_crypto_screen(page, username):
    recipient_field = ft.TextField(label="Recipient", width=150)
    asset_field = ft.Dropdown(
        label="Asset",
        options=[
            ft.dropdown.Option("BTC"),
            ft.dropdown.Option("ETH"),
            ft.dropdown.Option("SOL"),
        ],
        width=150,
    )
    amount_field = ft.TextField(label="Amount", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_send():
        recipient = recipient_field.value.strip().lstrip("@")
        asset = asset_field.value

        if not recipient:
            status_message.value = "Please enter recipient username"
            return
        if not asset:
            status_message.value = "Please select an asset"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        result = crypto_transfers.send_crypto(username, recipient, asset, amount)
        if not result:
            status_message.value = (
                "Transfer failed. Check recipient, balance, or 0.01 ETH gas."
            )
        else:
            go_back(page, username, content=crypto_screen)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Recipient", width=70), recipient_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Asset", width=70), asset_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    "Gas fee: 0.01 ETH per transfer", size=12, color=ft.Colors.GREY
                ),
                ft.Row([status_message], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Button("Send", on_click=handle_send),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=crypto_screen
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
    )


def stake_screen(page, username):
    asset_field = ft.Dropdown(
        label="Asset",
        options=[
            ft.dropdown.Option("BTC"),
            ft.dropdown.Option("ETH"),
            ft.dropdown.Option("SOL"),
        ],
        width=150,
    )
    amount_field = ft.TextField(label="Amount", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_stake():
        asset = asset_field.value
        if not asset:
            status_message.value = "Please select an asset"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        result = staking.stake_crypto(username, asset, amount)
        if not result:
            status_message.value = "Staking failed. Check available balance."
        else:
            go_back(page, username, content=crypto_screen)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Asset", width=70), asset_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([status_message], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Button("Stake", on_click=handle_stake),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=crypto_screen
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
    )


def crypto_screen(page, username):
    db = persistence.load_db()
    user = db[username]
    crypto_txs = user["wallet"]["transactions"]
    eth_balance = user["wallet"]["assets"]["ETH"]
    sol_balance = user["wallet"]["assets"]["SOL"]
    btc_balance = user["wallet"]["assets"]["BTC"]
    command_field = ft.TextField(hint_text="try: send 0.5 BTC to @john", width=300)
    status_message = ft.Text("", color=ft.Colors.RED)

    def crypto_screen_loader():
        page.clean()
        page.add(send_crypto_screen(page, username))

    return ft.Container(
        # bgcolor=ft.Colors.GREY,
        content=ft.Column(
            [
                ft.Row(
                    [
                        asset_card(
                            "BTC",
                            btc_balance,
                            "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
                        ),
                        asset_card(
                            "ETH",
                            eth_balance,
                            "https://cryptologos.cc/logos/ethereum-eth-logo.png",
                        ),
                        asset_card(
                            "SOL",
                            sol_balance,
                            "https://cryptologos.cc/logos/solana-sol-logo.png",
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                ft.Row(
                    [
                        ft.Column(
                            controls=[
                                ft.Container(
                                    command_field, padding=ft.Padding.only(top=10)
                                ),
                                ft.Container(status_message),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Button("+", on_click=None),
                                        ft.Text("Add"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button("->", on_click=crypto_screen_loader),
                                        ft.Text("Send"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button("x", on_click=None),
                                        ft.Text("Stake"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text("Transactions"),
                        ft.Column(
                            [
                                *(
                                    ft.Text(
                                        f"{crypto_txs[i]['type']} {crypto_txs[i]['amount']} {crypto_txs[i]['asset']} on {crypto_txs[i]['date']}",
                                    )
                                    for i in range(len(crypto_txs) - 1, -1, -1)
                                )
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                        ),
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ]
        ),
    )
