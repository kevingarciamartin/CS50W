greeting = input('Greeting: ')

if 'hello' in greeting.lower():
    ind = greeting.lower().find('hello')
    if greeting[:ind].isspace():
        print('$0')
elif 'h' in greeting.lower():
    ind = greeting.lower().find('h')
    if greeting[:ind].isspace():
        print('$20')
else:
    print('$100')
