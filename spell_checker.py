
def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Strings must have equal length")

    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

def indel_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    if len_str1 == 0:
        return len_str2
    if len_str2 == 0:
        return len_str1
    
    if str1[0] == str2[0]:
        return indel_distance(str1[1:], str2[1:])
    
    return 1 + min(indel_distance(str1, str2[1:]), indel_distance(str1[1:], str2))


def modified_levenshtein_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    if len_str1 == 0:
        return len_str2
    if len_str2 == 0:
        return len_str1
    
    substitution_cost = 0.5 if str1[0] != str2[0] else 0
    insertion_deletion_cost = 1.0
    
    # Check if the letters are close on the keyboard
    if str1[0] == 'p' and str2[0] == 'o':
        substitution_cost = 0.2
    elif str1[0] == 'o' and str2[0] == 'p':
        substitution_cost = 0.2
    elif str1[0] == 'a' and str2[0] == 's':
        substitution_cost = 0.2
    elif str1[0] == 's' and str2[0] == 'a':
        substitution_cost = 0.2
    
    return min(
        modified_levenshtein_distance(str1[1:], str2) + insertion_deletion_cost,
        modified_levenshtein_distance(str1, str2[1:]) + insertion_deletion_cost,
        modified_levenshtein_distance(str1[1:], str2[1:]) + substitution_cost
    )


def modified_hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Strings must have equal length")

    distance = 0
    
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            # Check if the letters are close on the keyboard
            if c1 == 'p' and c2 == 'o':
                distance += 0.25
            elif c1 == 'o' and c2 == 'p':
                distance += 0.25
            elif c1 == 'a' and c2 == 's':
                distance += 0.25
            elif c1 == 's' and c2 == 'a':
                distance += 0.25
            else:
                distance += 0.5
    
    return distance


def suggest_correct_word(incorrect_word):
    with open("words_alpha.txt", "r") as file:
        words = file.read().splitlines()

    min_distance = float("inf")
    correct_word = None

    for word in words:
        distance = levenshtein_distance(incorrect_word, word)
        if distance < min_distance:
            min_distance = distance
            correct_word = word

    return correct_word


def spell_check_text_file(input_file, output_file):
    with open(input_file, "r") as file:
        text = file.read()

    corrected_words = []
    for word in text.split():
        corrected_word = suggest_correct_word(word.lower())
        corrected_words.append(corrected_word)

    corrected_text = " ".join(corrected_words)

    with open(output_file, "w") as file:
        file.write(corrected_text)

# Test Levenshtein distance
levenshtein_result_1 = levenshtein_distance("kitten", "sitting")
levenshtein_result_2 = levenshtein_distance("Saturday", "Sunday")
levenshtein_result_3 = levenshtein_distance("book", "back")

print(f"Levenshtein distance test 1: {levenshtein_result_1}")
print(f"Levenshtein distance test 2: {levenshtein_result_2}")
print(f"Levenshtein distance test 3: {levenshtein_result_3}")

# Test Hamming distance
hamming_result_1 = hamming_distance("karolin", "kathrin")
hamming_result_2 = hamming_distance("karolin", "karolin")
hamming_result_3 = hamming_distance("book", "back")

print(f"Hamming distance test 1: {hamming_result_1}")
print(f"Hamming distance test 2: {hamming_result_2}")
print(f"Hamming distance test 3: {hamming_result_3}")

# Test Modified Levenshtein distance
mod_levenshtein_result_1 = modified_levenshtein_distance("kitten", "sitting")
mod_levenshtein_result_2 = modified_levenshtein_distance("Saturday", "Sunday")
mod_levenshtein_result_3 = modified_levenshtein_distance("book", "back")
levenshtein_result_3 = levenshtein_distance("book", "back")

print(f"Modified Levenshtein distance test 1: {mod_levenshtein_result_1}")
print(f"Modified Levenshtein distance test 2: {mod_levenshtein_result_2}")
print(f"Modified Levenshtein distance test 3: {mod_levenshtein_result_3}")

# Test Indel distance
indel_result_1 = indel_distance("kitten", "sitting")
indel_result_2 = indel_distance("Saturday", "Sunday")
indel_result_3 = indel_distance("book", "back")

print(f"Indel distance test 1: {indel_result_1}")
print(f"Indel distance test 2: {indel_result_2}")
print(f"Indel distance test 3: {indel_result_3}")

# Test modified Hamming distance
mod_hamming_result_1 = modified_hamming_distance("karolin", "kathrin")
mod_hamming_result_2 = modified_hamming_distance("karolin", "karolin")
mod_hamming_result_3 = modified_hamming_distance("book", "back")

print(f"Modified Hamming distance test 1: {mod_hamming_result_1}")
print(f"Modified Hamming distance test 2: {mod_hamming_result_2}")
print(f"Modified Hamming distance test 3: {mod_hamming_result_3}")

# Test suggesting correct word
correct_word_1 = suggest_correct_word("acress")
correct_word_2 = suggest_correct_word("librery")
correct_word_3 = suggest_correct_word("comitte")

print(f"Suggested correct word test 1: {correct_word_1}")
print(f"Suggested correct word test 2: {correct_word_2}")
print(f"Suggested correct word test 3: {correct_word_3}")

spell_check_text_file("to_check.txt", "checked.txt")

