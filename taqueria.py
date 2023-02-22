# Create menu dictionary
menu = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

# Set current price to 0
total_amount = 0

# Loop forever
while True:

    # Try
    try:

        # Get user input
        item = input('Item: ').title()

        # Check if item is already in dictionary
        if item in menu:

            # Add the item price to current price
            total_amount += menu[item]

            # Print the current price
            print('Total: ${:0.2f}'.format(total_amount))

    # Except
    except EOFError:

        # Print a new line and stop the loop
        print()
        break