# TODO

def main():
    # Prompt for height
    while True:
        height = int(input('Height: '))
        if height >= 1 and height <= 8:
            break

    # Print pyramid
    for i in range(height):
        for j in range(height):
            if j >= height - 1 - i:
                print('#', end = '')
            else:
                print(' ', end = '')
        print()




main()