from cs50 import get_int
import re

def main():
    card = get_int("Enter card number: ")
    card_str = str(card)
    check_sum = checksum(card_str)
    if check_sum:
        print(f"{checkdigits(card_str)}")
    else:
        print("INVALID")




#Check first two digits
def checkdigits(card_str):
    card_length = len(card_str)
    if re.match(r"^34|^37", card_str) and card_length == 15:
        return "AMEX"
    elif re.match(r"^51|^52|^53|^54|^55", card_str) and card_length == 16:
        return "MASTERCARD"
    elif re.match(r"^4", card_str) and (card_length == 13 or card_length == 16):
        return "VISA"
    else:
        return "INVALID"


#Perform Checksum

def checksum(card_str):
    total_sum = 0
    length = len(card_str)
    for i in range(length):
        digit = int(card_str[length - 1 - i])
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total_sum += digit

    return total_sum % 10 == 0


main()
