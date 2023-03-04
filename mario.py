# TODO

import cs50


def main():
    # Prompt for height
    while True:
        height = cs50.get_int('Height: ')
        if height >= 1 and height <= 8:
            break

    # Print pyramids
    for i in range(height):
        for j in range(2 * height):
            # Right-aligned pyramid
            if j >= height - 1 - i:
                # Left-aligned pyramid
                if j > height + i:
                    break
                print('#', end='')
            else:
                print(' ', end='')

            # Make gap between pyramids
            if j == height - 1:
                for k in range(2):
                    print(' ', end='')
        print()


main()