# TODO

from cs50 import get_string
import re


def main():
    # Prompt user for text
    text = get_string('Text: ')

    # Analyze text
    numLetters = count_letters(text)
    numWords = count_words(text)
    numSentences = count_sentences(text)

    # Coleman-Liau index
    L = numLetters / numWords * 100
    S = numSentences / numWords * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Print grade level
    if index < 1:
        print('Before Grade 1')
    elif index >= 16:
        print('Grade 16+')
    else:
        print(f'Grade {index}')


def count_letters(text):
    # Count amount of letters in text
    alphanum = [c.lower() for c in text if c.isalpha()]
    letters = len(alphanum)
    return letters


def count_words(text):
    # Count amount of words in text
    words = len(text.split())
    return words


def count_sentences(text):
    # Count amount of sentences in text
    sentences = len(re.split(r'[.!?]+', text)) - 1
    return sentences


main()