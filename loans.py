import datetime

import persistence

MAX_LOANS_ALLOWED = 2
MAX_LOAN_AMOUNT_PKR = 50000
DEFAULT_LOAN_DURATION_DAYS = 7
INTEREST_RATE = 0.13


def request_loan(
    username,
    amount,
    currency="PKR",
    term=DEFAULT_LOAN_DURATION_DAYS,
    interest_rate=INTEREST_RATE,
):
    if amount <= 0 or amount > MAX_LOAN_AMOUNT_PKR:
        return False

    if term < 7:
        return False

    currency = currency.upper()
    if currency != "PKR":
        return False

    db = persistence.load_db()

    if username not in db:
        return False
    loans = db[username]["loans"]

    if len(loans) >= MAX_LOANS_ALLOWED:
        return False

    this_loan_due_date = (
        datetime.datetime.now() + datetime.timedelta(days=term)
    ).strftime("%Y-%m-%d")

    db[username]["fiat"]["balances"]["PKR"] += amount

    loans.append(
        {
            "amount": amount,
            "interest_rate": interest_rate,
            "due_date": this_loan_due_date,
        }
    )

    db[username]["fiat"]["transactions"].append(
        {
            "id": len(db[username]["fiat"]["transactions"]) + 1,
            "type": "loan disbursement",
            "amount": amount,
            "currency": currency,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    )

    persistence.save_db(db)
    return True


def payback(username, loan_index):
    db = persistence.load_db()

    if username not in db:
        return False
    loans = db[username]["loans"]

    if loan_index < 0 or loan_index >= len(loans):
        return False

    loan = loans[loan_index]

    payback_amount = loan["amount"] + calculate_interest(loan)

    if db[username]["fiat"]["balances"]["PKR"] < payback_amount:
        return False

    db[username]["fiat"]["balances"]["PKR"] -= payback_amount

    db[username]["fiat"]["transactions"].append(
        {
            "id": len(db[username]["fiat"]["transactions"]) + 1,
            "type": "loan repayment",
            "amount": payback_amount,
            "currency": "PKR",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    )
    loans.pop(loan_index)

    persistence.save_db(db)
    return True


def calculate_interest(loan):
    default = loan["amount"] * loan["interest_rate"]

    # Calculate the number of days past due
    due_date = datetime.datetime.strptime(loan["due_date"], "%Y-%m-%d")
    days_past_due = (datetime.datetime.now() - due_date).days

    if days_past_due > 0:
        # apply additional interest for overdue loans
        overdue_interest = loan["amount"] * loan["interest_rate"] * days_past_due
        return default + overdue_interest
    return default
