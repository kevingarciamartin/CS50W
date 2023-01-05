#include <cs50.h>
#include <stdio.h>
#include <math.h>

long get_crednum(void);
bool check_digits(long crednum);
bool check_luhn(long crednum);

int main(void)
{
    // Ask what credit card number the user has
    long crednum = get_crednum();
}

long get_crednum(void)
{
    // Prompt for credit card number
    long crednum;
    bool digits;
    do
    {
        crednum = get_long("Number: ");

        // Check digits in number
        digits = check_digits(crednum);
    }
    while (digits == false);

    return 0;
}

bool check_digits(long crednum)
{
    // Check Luhn's algorithm
    bool luhn = check_luhn(crednum);
    if (luhn == false)
    {
        return false;
    }

    // Get first two digits from number
    long digs = crednum;
    while (digs > 100)
    {
        digs = digs / 10;
    }

    // Check amount of digits in number
    if (crednum >= pow(10,12) && crednum < pow(10,16))
    {
        if (crednum >= pow(10,15))
        {
            if (digs == 51 || digs == 52 || digs == 53 || digs == 54 || digs == 55)
            {
                if (luhn == true)
                {
                    printf("MASTERCARD\n");
                    return true;
                }
            }
            if (digs / 10 == 4)
            {
                if (luhn == true)
                {
                    printf("VISA\n");
                    return true;
                }
            }
        }
        else if (crednum >= pow(10,14))
        {
            if (digs == 34 || digs == 37)
            {
                if (luhn == true)
                {
                    printf("AMEX\n");
                    return true;
                }
            }
            else
            {
                printf("INVALID\n");
            }
        }
        if (digs / 10 == 4)
        {
            if (luhn == true)
            {
                printf("VISA\n");
                return true;
            }
        }
        printf("INVALID\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}

bool check_luhn(long crednum)
{
    long num = crednum;
    int sum = 0;
    sum = num % 10;                                 // add rightmost digit to checksum
    num = num / 10;                                 // discard rightmost digit

    while (num)
    {
        int temp = (num % 10) * 2;                  // get rightmost digit and double
        if (temp > 9)                               // if 2 digit number, add digits together
        {
            temp = (temp / 10) + (temp % 10);
        }
        sum += temp;                                // add digit to checksum
        num = num / 10;                             // discard rightmost digit
        temp = num % 10;                            // get rightmost digit
        sum += temp;                                // add non-multiplied digit to checksum
        num = num / 10;                             // discard rightmost digit
    }
    return (sum % 10 == 0);
}