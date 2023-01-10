#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);
int decimalToBinary(char ch);
int decimalToBinary2(char ch);

int main(void)
{
    // TODO

    // Prompt user for message
    string message = get_string("Message: ");

    // Convert message into a series of 8-bit binary numbers, one for each character of the string
    for (int i = 0; i < strlen(message); i++)
    {
        int binary = decimalToBinary2(message[i]);
        // Store digits in array in reverse order, adding missing zeros if necessary
        int binReverse[BITS_IN_BYTE] = {0};
        int temp = binary;
        int bit;
        int j = 0;
        while (binary != 0)
        {
            bit = temp % 2;
            temp /= 10;
            binReverse[j] = bit;
            j++;
        }
        // Print bulbs in groups of eight
        for (int k = BITS_IN_BYTE - 1; k >= 0; k--)
        {
            print_bulb(binReverse[k]);
        }
        // Print new line
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}

int decimalToBinary(char ch)
{
    int binary[BITS_IN_BYTE];
    int i = 0;
    int dec = ch;
    while (dec > 0)
    {
            binary[i++] = dec % 2;
            dec /= 2;
    }
    return 0;
}

int decimalToBinary2(char ch)
{
    int dec = ch;
    long binary = 0;
    int cnt = 0;
    while (dec != 0)
    {
        int rem = dec % 2;
        long c = pow(10, cnt);
        binary += rem * c;
        dec /= 2;
        cnt++;
    }
    return binary;
}