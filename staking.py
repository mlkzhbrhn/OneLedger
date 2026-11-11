# staking feature for crypto wallets

# staking yield calculator using recursion (compound interest formula)
def calculate_staking_yield(principal, rate, days):
    if days == 0:
        return principal
    else:
        next_day_principal = principal * (1 + rate / 100)
        return calculate_staking_yield(next_day_principal, rate, days - 1) 