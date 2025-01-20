#include <stdio.h>
#include <cs50.h>

bool luhn_function(long card_number);
string card_type(long card_number);

int main(void)
{
    long card_number = get_long("Number: ");

    if (luhn_function(card_number))
    {
        printf("%s\n", card_type(card_number));
    }
    else
    {
        printf("INVALID\n");
    }
}


bool luhn_function(long card_number)
{
    int sum = 0;
    bool alternate = false;

    while (card_number > 0)
    {
        int digit = card_number % 10;
        card_number /= 10;

        if (alternate)
        {
            digit *= 2;
            sum += (digit % 10) + (digit / 10);
        }
        else
        {
            sum += digit;
        }

        alternate = !alternate;
    }

    return (sum % 10) == 0;
}

string card_type(long card_number)
{
    int first_digit = 0, first_two_digits = 0, length = 0;
    long temp = card_number;

    while (temp > 0)
    {
        first_digit = temp % 10;
        if (temp < 100 && temp > 9)
        {
            first_two_digits = temp;
        }
        temp /= 10;
        length++;
    }

    if ((first_two_digits == 34 || first_two_digits == 37) && length == 15)
    {
        return "AMEX";
    }
    else if ((first_two_digits >= 51 && first_two_digits <= 55) && length == 16)
    {
        return "MASTERCARD";
    }
    else if (first_digit == 4 && (length == 13 || length == 16))
    {
        return "VISA";
    }
    return "INVALID";
}
