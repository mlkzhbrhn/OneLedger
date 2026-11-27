import flet as ft

import loans
import persistence
from ui_helpers import asset_card, go_back, screen_loader


def request_loan_screen(page, username):
    amount_field = ft.TextField(label="Amount (PKR)", width=150)
    term_field = ft.TextField(
        label="Term (Days)",
        value=str(loans.DEFAULT_LOAN_DURATION_DAYS),
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_request():
        try:
            amount = float(amount_field.value)
        except (TypeError, ValueError):
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0 or amount > loans.MAX_LOAN_AMOUNT_PKR:
            status_message.value = (
                f"Amount must be between 1 and {loans.MAX_LOAN_AMOUNT_PKR} PKR"
            )
            return

        try:
            term = int(term_field.value)
        except (TypeError, ValueError):
            status_message.value = "Please enter a valid number of days"
            return

        if term < loans.DEFAULT_LOAN_DURATION_DAYS:
            status_message.value = (
                f"Minimum loan term is {loans.DEFAULT_LOAN_DURATION_DAYS} days"
            )
            return

        result = loans.request_loan(username, amount, term=term)
        if not result:
            status_message.value = (
                f"Loan request failed. Max {loans.MAX_LOANS_ALLOWED} active loans allowed."
            )
        else:
            go_back(page, username, content=loans_screen)

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Term", width=70), term_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    f"Max {loans.MAX_LOAN_AMOUNT_PKR} PKR • {int(loans.INTEREST_RATE * 100)}% interest • Max {loans.MAX_LOANS_ALLOWED} active loans",
                    size=12,
                    color=ft.Colors.GREY,
                ),
                ft.Row([status_message], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        ft.Button("Request Loan", on_click=handle_request),
                        ft.Button(
                            "Cancel",
                            on_click=lambda: go_back(
                                page, username, content=loans_screen
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


def loans_screen(page, username):
    db = persistence.load_db()
    user = db[username]
    pkr_balance = user["fiat"]["balances"]["PKR"]
    active_loans = user["loans"]
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_payback(loan_index):
        result = loans.payback(username, loan_index)
        if not result:
            status_message.value = "Repayment failed. Check your PKR balance."
        else:
            go_back(page, username, content=loans_screen)

    loan_cards = [
        ft.Container(
            padding=12,
            margin=ft.Margin.only(bottom=8),
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                f"Loan #{idx + 1}: {loan['amount']:.2f} PKR",
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Interest: {loans.calculate_interest(loan):.2f} PKR • "
                                f"Total Due: {loan['amount'] + loans.calculate_interest(loan):.2f} PKR",
                                size=12,
                            ),
                            ft.Text(
                                f"Due Date: {loan['due_date']}",
                                size=12,
                                color=ft.Colors.GREY,
                            ),
                        ],
                        spacing=4,
                    ),
                    ft.Button(
                        "Pay Back",
                        on_click=lambda _, i=idx: handle_payback(i),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        for idx, loan in enumerate(active_loans)
    ]

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        asset_card(
                            "PKR", pkr_balance, "https://flagcdn.com/w80/pk.png"
                        ),
                        ft.Column(
                            [
                                ft.Button(
                                    "+",
                                    on_click=lambda: screen_loader(
                                        page, request_loan_screen, username
                                    ),
                                ),
                                ft.Text("Request Loan"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                status_message,
                ft.Divider(),
                ft.Text(
                    f"Active Loans ({len(active_loans)}/{loans.MAX_LOANS_ALLOWED})",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Column(
                    loan_cards if loan_cards else [ft.Text("No active loans.")],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ]
        ),
        padding=10,
        expand=True,
    )
