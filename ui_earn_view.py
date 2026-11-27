import flet as ft

import persistence
import points
import savings
import staking
from ui_helpers import asset_card, go_back, screen_loader


def redeem_points_screen(page, username):
    db = persistence.load_db()
    user_points = db[username].get("points", 0)
    points_field = ft.TextField(label="Points", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_redeem():
        try:
            amount = int(points_field.value)
        except (TypeError, ValueError):
            status_message.value = "Please enter a valid whole number of points"
            return

        if amount < points.MIN_REDEEM_POINTS:
            status_message.value = (
                f"Minimum redemption is {points.MIN_REDEEM_POINTS} points"
            )
            return

        result = points.redeem_points(username, amount)
        if not result:
            status_message.value = "Redemption failed. Check your points balance."
        else:
            go_back(page, username, content=earn_screen)

    return ft.Container(
        ft.Column(
            [
                ft.Text(
                    f"Available: {user_points} points (1 point = {points.PKR_PER_POINT} PKR)",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    [ft.Text("Points", width=70), points_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    f"Minimum {points.MIN_REDEEM_POINTS} points to redeem to PKR",
                    size=12,
                    color=ft.Colors.GREY,
                ),
                ft.Row([status_message], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Button("Redeem", on_click=handle_redeem),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=earn_screen
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


def staking_action_screen(page, username, mode="unstake"):
    is_stake = mode == "stake"
    action_label = "Stake" if is_stake else "Unstake"
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

    def handle_submit():
        asset = asset_field.value
        if not asset:
            status_message.value = "Please select an asset"
            return

        try:
            amount = float(amount_field.value)
        except (TypeError, ValueError):
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        if is_stake:
            result = staking.stake_crypto(username, asset, amount)
            fail_msg = "Staking failed. Check available wallet balance."
        else:
            result = staking.unstake_crypto(username, asset, amount)
            fail_msg = "Unstaking failed. Check staked balance."

        if not result:
            status_message.value = fail_msg
        else:
            go_back(page, username, content=earn_screen)

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
                        ft.Button(action_label, on_click=handle_submit),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=earn_screen
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


def savings_action_screen(page, username, mode="deposit"):
    is_deposit = mode == "deposit"
    action_label = "Save" if is_deposit else "Withdraw"
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    amount_field = ft.TextField(label="Amount", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_submit():
        currency = currency_field.value
        if not currency:
            status_message.value = "Please select currency"
            return

        try:
            amount = float(amount_field.value)
        except (TypeError, ValueError):
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        if is_deposit:
            result = savings.deposit_to_savings(username, amount, currency)
            fail_msg = "Failed to deposit to savings. Check your fiat balance."
        else:
            result = savings.withdraw_from_savings(username, amount, currency)
            fail_msg = "Failed to withdraw from savings. Check your savings balance."

        if not result:
            status_message.value = fail_msg
        else:
            go_back(page, username, content=earn_screen)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Currency", width=70), currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([status_message], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Button(action_label, on_click=handle_submit),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=earn_screen
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
    user_points = user.get("points", 0)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Staked Crypto", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Button(
                                            "+",
                                            on_click=lambda: screen_loader(
                                                page,
                                                lambda p, u: staking_action_screen(
                                                    p, u, mode="stake"
                                                ),
                                                username,
                                            ),
                                        ),
                                        ft.Text("Stake"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button(
                                            "-",
                                            on_click=lambda: screen_loader(
                                                page,
                                                lambda p, u: staking_action_screen(
                                                    p, u, mode="unstake"
                                                ),
                                                username,
                                            ),
                                        ),
                                        ft.Text("Unstake"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
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
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Button(
                                            "+",
                                            on_click=lambda: screen_loader(
                                                page,
                                                lambda page, username: (
                                                    savings_action_screen(
                                                        page, username, mode="deposit"
                                                    )
                                                ),
                                                username,
                                            ),
                                        ),
                                        ft.Text("Save"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button(
                                            "-",
                                            on_click=lambda: screen_loader(
                                                page,
                                                lambda page, username: (
                                                    savings_action_screen(
                                                        page, username, mode="withdraw"
                                                    )
                                                ),
                                                username,
                                            ),
                                        ),
                                        ft.Text("Withdraw"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ]
                        ),
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
                ft.Divider(),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Reward Points",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{user_points} pts (= {user_points * points.PKR_PER_POINT} PKR)",
                                    size=14,
                                ),
                            ],
                            spacing=4,
                        ),
                        ft.Button(
                            "Redeem",
                            on_click=lambda: screen_loader(
                                page, redeem_points_screen, username
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=10,
        expand=True,
    )
