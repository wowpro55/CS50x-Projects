    second_digits = [int(card_str[i])*2 for i in range(1, len(card_str), 2)]
    second_digits2 = []
    for number in second_digits:
        for digit in str(number):
            second_digits2.append(int(digit))


def checksum(card_str):
    length = len(card_str)
    second_digits = [int(card_str[i])*2 for i in range(length -1, -1, -2)]
    second_digits2 = []
    for number in second_digits:
        for digit in str(number):
            second_digits2.append(int(digit))
    first_digits = sum([int(card_str[i]) for i in range(length, -1, -2)])
    checksum = str(sum(second_digits2) + first_digits)
    if int(checksum) % 10 == 0:
        return True
    else:
        return False
