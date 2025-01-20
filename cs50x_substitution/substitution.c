#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


bool is_valid_key(string key);
string substitute(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (!is_valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = substitute(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}
bool is_valid_key(string key)
{
    // Check key length
    if (strlen(key) != 26)
    {
        return false;
    }

    bool seen[26] = {false};
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = tolower(key[i]) - 'a';
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }

    return true;
}

string substitute(string plaintext, string key)
{
    string ciphertext = plaintext;

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            bool is_upper = isupper(plaintext[i]);
            int index = tolower(plaintext[i]) - 'a';
            char substitute_char = is_upper ? toupper(key[index]) : tolower(key[index]);
            ciphertext[i] = substitute_char;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    return ciphertext;
}
