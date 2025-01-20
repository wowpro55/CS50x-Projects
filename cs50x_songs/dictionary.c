// Implements a dictionary's functionality

#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

void unload_recursion(node *p);

// TODO: Choose number of buckets in hash table
const unsigned int N = 150001;

// Number of words loaded from dictionary
int j;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int h;
    int l;
    node *p;
    char word_check[LENGTH + 1];
    for (l = 0; word[l] != '\0'; l++)
    {
        if (isalpha(word[l]) != 0)
            word_check[l] = tolower(word[l]);
        else
            word_check[l] = word[l];
    }
    word_check[l] = '\0';
    h = hash(word_check);
    p = table[h];
    for (p = table[h]; p != NULL; p = p->next)
    {
        if (strcmp(p->word, word_check) == 0)
            return true;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    int k;
    for (k = 0; word[k] != '\0'; k++)
    {
        sum += word[k];
    }
    return (strlen(word) + sum) % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    // Initializing table
    for (int m = 0; m < 150001; m++)
    {
        table[m] = NULL;
    }

    // Open dictionary for read
    FILE *dic_input = fopen(dictionary, "r");
    if (dic_input == NULL)
    {
        printf("Dictionary could not be opened\n");
        return false;
    }
    int i = 0;
    char c = '\0';
    int h;

    // Iterate through dictionary and copy words
    for (j = -1; c != EOF; j++)
    {
        // Malloc new node each j-interation
        node *p = malloc(sizeof(node));
        p->next = NULL;
        if (p == NULL)
        {
            printf("Malloc malfunction\n");
            return false;
        }

        // Copy word into node
        while ((c = fgetc(dic_input)) != '\n' && c != EOF)
        {
            p->word[i] = c;
            i++;
        }
        p->word[i] = '\0';
        i = 0;

        // Hash the word
        h = hash(p->word);

        // Insert node into hash table

        // Connect hash table with new node
        if (table[h] == NULL)
            table[h] = p;
        else
        {
            p->next = table[h];
            table[h] = p;
        }
    }

    fclose(dic_input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return j;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    int s;
    for (s = 0; s < N; s++)
    {
        node *p = table[s];
        unload_recursion(p);
    }
    return true;
}

void unload_recursion(node *p)
{
    if (p == NULL)
    {
        return;
    }

    else
    {
        unload_recursion(p->next);
    }

    free(p);
}
