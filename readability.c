#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt user for text
    string text = get_string("Text: ");

    // Analyze text
    int numLetters = count_letters(text);
    int numWords = count_words(text);
    int numSentences = count_sentences(text);

    // Coleman-Liau index
    float L = (float) numLetters / numWords * 100;                // Average amount of letters per 100 words
    float S = (float) numSentences / numWords * 100;              // Average amount of sentences per 100 words
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // Count amount of letters in text
    int letters = 0;

    int i = 0;
    while (text[i] != '\0')
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            letters++;
        }
        i++;
    }
    return letters;
}

int count_words(string text)
{
    // Count amount of words in text
    int words = 0;

    int i = 0;
    while (text[i] != '\0')
    {
        if (text[i] == ' ')
        {
            if (text[i - 1] == ' ')
            {
                i++;
                continue;
            }
            words++;
        }
        i++;
    }

    // Add the last word of the sentence
    if (words > 0)
    {
        words++;
    }
    return words;
}

int count_sentences(string text)
{
    // Count amount of sentences in text
    int sentences = 0;

    int i = 0;
    while (text[i] != '\0')
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            if (isupper(text[i - 1]) || islower(text[i - 1]))
            {
                sentences++;
            }
        }
        i++;
    }
    return sentences;
}