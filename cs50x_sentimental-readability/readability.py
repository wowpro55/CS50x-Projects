from cs50 import get_string
from collections import Counter

def main():

    #get user input
    input = get_string("Text:")

    #Count number words
    list_words = Counter(input.split())
    sum_words = sum(list_words.values())

    #Count number letters
    cnt_letter = Counter(letter.lower() for letter in input if letter.isalpha())
    sum_letters = sum(cnt_letter.values())

    #Count number of sentences
    cnt_sentence = Counter(char for char in input if char in ".?!")
    sum_sentence = sum(cnt_sentence.values())

    #Calculate L
    l = (sum_letters / sum_words) * 100

    #Calculate S
    s = (sum_sentence / sum_words) * 100

    index = round(0.0588 * l - 0.296 * s - 15.8)

    if index >= 16:
        print ("Grade 16+")
    elif index < 1:
        print ("Before Grade 1")
    else:
        print(f"Grade {index}")

main()
