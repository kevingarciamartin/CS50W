# TODO

import cs50


def main():
    # Ask how much change the customer is owed
    cents = get_cents()

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents -= quarters * 25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents -= dimes * 10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(cents)
    cents -= nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)
    cents -= pennies

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


def get_cents():
    # Prompt for change
    while True:
        dollars = cs50.get_float('Change owed: ')
        if dollars >= 0:
            break
    cents = int(dollars * 100)
    return cents


def calculate_quarters(cents):
    # Calculate the number of quarters to give the customer
    quarters = int(cents / 25)
    return quarters


def calculate_dimes(cents):
    # Calculate the number of dimes to give the customer
    dimes = int(cents / 10)
    return dimes


def calculate_nickels(cents):
    # Calculate the number of nickels to give the customer
    nickels = int(cents / 5)
    return nickels


def calculate_pennies(cents):
    # Calculate the number of pennies to give the customer
    pennies = cents
    return pennies


main()