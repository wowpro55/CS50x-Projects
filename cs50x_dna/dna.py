import csv
import sys
import copy


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Please insert two command line arguments")
        sys.exit()

    # TODO: Read database file into a variable
    rows = []
    rows2 = []
    filename = sys.argv[1]

    #Create list of STRs
    with open(filename, 'r') as file:

        reader = csv.reader(file)
        first_row = next(reader)
        str_list = first_row[1:]

    #Read file into a dictionary (rows2) and rows without the name key
    with open(filename, 'r') as file:
        database = csv.DictReader(file)
        for row in database:

            #Create row2
            rows2.append(copy.deepcopy(row))

            #Create row
            row_copy = copy.deepcopy(row)
            first_key = list(row_copy.keys())[0]
            del row_copy[first_key]
            rows.append(row_copy)

    # TODO: Read DNA sequence file into a variable
    filename2 = sys.argv[2]
    with open(filename2, 'r') as file:
        dna = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    key_sequence = {}
    for key in str_list:
        key_sequence[key] = longest_match(dna, key)
    key_sequence = {key: str(value) for key, value in key_sequence.items()}

    # TODO: Check database for matching profiles
    length_list = len(rows)
    counter = 0
    for row in rows:
        if row == key_sequence:
            print(f"{rows2[counter]['name']}")
        counter += 1

    if length_list == counter:
            print('No match')

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
