from cs50 import get_string
from collections import Counter

def main():

    #get user input
    input = get_string("Text:")

    #Count number words
    list_words = input.split()
    number_words = Counter(list_words)

    #Count number letters
    cnt = Counter(letter.lower() for letter in input if isalpha())
    sum_letters = sum(cnt.values)

    print(f"{sum_letters}")


#Calculate L (average letters/100 words)

#Calculate S (average sentence/100 words )


#Implementation of the coleman-liau index






main()
