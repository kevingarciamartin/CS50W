#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

const int ALPH = 26;

int main(int argc, string argv[])
{
    // Print error message
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int i = 0;
    while (argv[1][i] != '\0')
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        i++;
    }

    // Extract key as int
    int n = i;
    int keyvec[n];
    i = 0;
    while (argv[1][i] != '\0')
    {
        keyvec[i] = argv[1][i] - '0';
        i++;
    }

    int key = 0;
    int cnt = 0;
    for (i = n - 1; i >= 0; i--)
    {
        int rem = keyvec[i] % 10;
        int c = pow(10, cnt);
        key += rem * c;
        cnt++;
    }

    // Prompt user for plaintext
    string plain = get_string("plaintext:  ");
    int m = strlen(plain);

    // Cipher text
    string cipher = plain;
    i = 0;
    while (cipher[i] != '\0')
    {
        if (isupper(cipher[i]))
        {
            cipher[i] -= 'A';
            cipher[i] = (plain[i] + key) % ALPH;
            cipher[i] += 'A';
        }
        else if (islower(cipher[i]))
        {
            cipher[i] -= 'a';
            cipher[i] = (plain[i] + key) % ALPH;
            cipher[i] += 'a';
        }
        i++;
    }

    // Print ciphertext
    printf("ciphertext: ");
    for (i = 0; i <= m; i++)
    {
        printf("%c", cipher[i]);
    }
    printf("\n");

    return 0;
}