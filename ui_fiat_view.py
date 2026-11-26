import asyncio

import flet as ft

import command_executor
import conversion
import deposit
import persistence
import transfer
import withdrawal
from ui_helpers import asset_card, go_back, screen_loader


def transfer_screen(page, username):
    recipient_field = ft.TextField(label="Recipient", width=150)
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_transfer():
        recipient = recipient_field.value.strip()
        currency = currency_field.value

        if not recipient:
            status_message.value = "Please enter recipient username"
            return
        if not currency:
            status_message.value = "Please select currency"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        result = transfer.transfer_funds(username, recipient, amount, currency)
        if not result:
            status_message.value = "Transfer failed. Check recipient or balance."
        else:
            go_back(page, username)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Recipient", width=70), recipient_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Currency", width=70), currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Transfer", on_click=handle_transfer),
                        ft.Button("Cancel", on_click=lambda: go_back(page, username)),
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


def withdrawal_screen(page, username):
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_withdrawal():
        currency = currency_field.value
        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if not amount:
            status_message.value = "Please enter amount"
        elif not currency:
            status_message.value = "Please select currency"

        result = withdrawal.withdrawal(username, amount, currency)
        if not result:
            status_message.value = "Error withdrawing funds. Please try again."
        else:
            status_message.value = "Withdrawal successful."
            go_back(page, username)

    withdrawal_page = ft.Container(
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
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Withdraw", on_click=handle_withdrawal),
                        ft.Button("Cancel", on_click=lambda: go_back(page, username)),
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

    return withdrawal_page


def deposit_screen(page, username):
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_deposit():
        currency = currency_field.value
        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if not amount:
            status_message.value = "Please enter amount"
        elif not currency:
            status_message.value = "Please select currency"

        result = deposit.deposit(username, amount, currency)
        if not result:
            status_message.value = "Error depositing funds. Please try again."
        else:
            status_message.value = "Deposit successful."
            go_back(page, username)

    deposit_page = ft.Container(
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
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Deposit", on_click=handle_deposit),
                        ft.Button("Cancel", on_click=lambda: go_back(page, username)),
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

    return deposit_page


def convert_screen(page, username):
    fiat_currency_field = ft.Dropdown(
        label="From (Fiat)",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    crypto_currency_field = ft.Dropdown(
        label="To (Crypto)",
        options=[
            ft.dropdown.Option("BTC"),
            ft.dropdown.Option("ETH"),
        ],
        width=150,
    )
    amount_field = ft.TextField(label="Fiat Amount", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)
    loader = ft.ProgressRing(visible=False, width=50, height=50)

    async def handle_convert():
        fiat_currency = fiat_currency_field.value
        crypto_currency = crypto_currency_field.value

        if not fiat_currency:
            status_message.value = "Please select fiat currency"
            return
        if not crypto_currency:
            status_message.value = "Please select crypto asset"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        loader.visible = True
        status_message.value = "Converting..."
        page.update()

        result = await asyncio.to_thread(
            conversion.convert_fiat_to_crypto,
            username,
            amount,
            fiat_currency,
            crypto_currency,
        )

        loader.visible = False

        if not result:
            status_message.value = "Conversion failed. Check balance or exchange rates."
        else:
            go_back(page, username)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("From", width=70), fiat_currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("To", width=70), crypto_currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [loader, status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Convert", on_click=handle_convert),
                        ft.Button("Cancel", on_click=lambda: go_back(page, username)),
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


def dashboard(page, username):
    db = persistence.load_db()
    user = db[username]
    fiat_txs = user["fiat"]["transactions"]
    pkr_balance = user["fiat"]["balances"]["PKR"]
    usd_balance = user["fiat"]["balances"]["USD"]

    def handle_command():
        command = command_field.value.strip()
        if not command:
            status_message.value = "Please enter a command"
            return

        result = command_executor.execute_command(username, command)
        if not result:
            status_message.value = "Transfer failed."
        else:
            status_message.value = "Transfer successful."

    command_field = ft.TextField(
        hint_text="try: send 500 PKR to @john", width=300, on_submit=handle_command
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        asset_card(
                            "PKR", pkr_balance, "https://flagcdn.com/w80/pk.png"
                        ),
                        asset_card(
                            "USD", usd_balance, "https://flagcdn.com/w80/us.png"
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
                                        ft.Button(
                                            "+",
                                            on_click=lambda: screen_loader(
                                                page, deposit_screen, username
                                            ),
                                        ),
                                        ft.Text("Deposit"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button(
                                            "-",
                                            on_click=lambda: screen_loader(
                                                page, withdrawal_screen, username
                                            ),
                                        ),
                                        ft.Text("Withdraw"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button(
                                            "->",
                                            on_click=lambda: screen_loader(
                                                page, transfer_screen, username
                                            ),
                                        ),
                                        ft.Text("Transfer"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button(
                                            "x",
                                            on_click=lambda: screen_loader(
                                                page, convert_screen, username
                                            ),
                                        ),
                                        ft.Text("Convert"),
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
                                        f"{fiat_txs[i]['type']} {fiat_txs[i]['amount']} {fiat_txs[i]['currency']} on {fiat_txs[i]['date']}",
                                    )
                                    for i in range(len(fiat_txs) - 1, -1, -1)
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
