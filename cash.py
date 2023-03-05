# TODO

import cs50


def main():
    # Ask how much change the customer is owed
    dollars = get_dollars()

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(dollars)
    dollars -= quarters * 0.25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(dollars)
    dollars -= dimes * 0.10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(dollars)
    dollars -= nickels * 0.05

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(dollars)
    dollars -= pennies * 0.01

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


def get_dollars():
    # Prompt for change
    while True:
        dollars = cs50.get_float('Change owed: ')
        if dollars >= 0:
            break
    return dollars


def calculate_quarters(dollars):
    # Calculate the number of quarters to give the customer
    quarters = int(dollars * 4)
    return quarters


def calculate_dimes(dollars):
    # Calculate the number of dimes to give the customer
    dimes = int(dollars * 10)
    return dimes


def calculate_nickels(dollars):
    # Calculate the number of nickels to give the customer
    nickels = int(dollars * 20)
    return nickels


def calculate_pennies(dollars):
    # Calculate the number of pennies to give the customer
    pennies = int(dollars * 100)
    return pennies


main()