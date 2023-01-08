#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

bool check(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (check(password))
    {
        printf("Your password is valid!\n");
    }
}

bool check(string password)
{
    bool upper = false;
    bool lower = false;
    bool number = false;
    bool symbol = false;

    int i = 0;
    while (password[i] != '\0')
    {
        if (isupper(password[i]))
        {
            upper = true;
        }
        else if (islower(password[i]))
        {
            lower = true;
        }
        else if (isdigit(password[i]))
        {
            number = true;
        }
        else if (ispunct(password[i]))
        {
            symbol = true;
        }
        i++;
    }

    if (upper && lower && number && symbol)
    {
        return true;
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol!\n");
        return false;
    }
}