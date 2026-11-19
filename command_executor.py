from nlp import command_parser
from transfer import transfer_funds
from deposit import deposit
from withdrawal import withdrawal

def execute_command(username, text):
    commands = command_parser(text)

    if not commands:
        return False

    action = commands[0]

    if action in ["send", "transfer"]:
        amount = float(commands[1])
        currency = commands[2].upper()
        recipient = (commands[4] if len(commands) > 4 else commands[3]).lstrip("@")
        return transfer_funds(username, recipient, amount, currency)

    if action in ["deposit", "withdraw"]:
        amount = float(commands[1])
        currency = commands[2].upper()
        if action == "deposit":
            return deposit(username, amount, currency)
        else:
            return withdrawal(username, amount, currency)

    return False
