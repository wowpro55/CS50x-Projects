#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int POINTS[] = {
    1, 3, 3, 2, 1, 4, 2, 4, 1, 8,
    5, 1, 3, 1, 1, 3, 10, 1, 1, 1,
    1, 4, 4, 8, 4, 10
};

int compute_score(string word);

int main(void)
{
    string player1_word = get_string("Player 1: ");

    string player2_word = get_string("Player 2: ");

    int score1 = compute_score(player1_word);
    int score2 = compute_score(player2_word);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int score = 0;

    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isalpha(word[i]))
        {
            char uppercase_letter = toupper(word[i]);
            score += POINTS[uppercase_letter - 'A'];
        }
    }

    return score;
}
