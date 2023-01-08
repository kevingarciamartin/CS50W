// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>

string replace(string input);

int main(int argc, string argv[])
{
    if (argc < 2)
    {
        printf("Missing command-line argument\n");
        return 1;
    }
    else if (argc > 2)
    {
        printf("Too many command-line arguments\n");
        return 1;
    }

    string output = replace(argv[1]);
    printf("%s\n", output);
}

string replace(string input)
{
    int i = 0;
    while (input[i] != '\0')
    {
        switch (input[i])
        {
            case 'a':
            input[i] = '6';
            break;

            case 'e':
            input[i] = '3';
            break;

            case 'i':
            input[i] = '1';
            break;

            case 'o':
            input[i] = '0';
            break;

            default:
            break;
        }

        i++;
    }
    
    return input;
}
