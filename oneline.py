def count_two_character_matches(a, b):
    string_b = len(b)
    counter = 0
    letter_count = 0
    for i in a:
        while counter + 1 < string_b:
            if (a[counter] == b[counter]) & (a[counter+1] == b[counter+1]):
                letter_count += 1
            counter += 1
    return letter_count