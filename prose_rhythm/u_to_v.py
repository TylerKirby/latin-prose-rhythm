"""
Convert U to V
Rules:
vowel + u = v (except au, which is a diphthong.
consonant + u = u
consonant + u + u + consonant = both u's are vowels
consonant + u + u + vowel = first u is V, second stays u

Rules for at the start of words:
u + consonant = u
u + vowel = v
"""

VOWELS = ["a", "e", "i", "o", "u"]

def convert_u_to_v(word):
    """
    Convert u in word to v.
    :param word: string
    :return: string
    """
    word = list(word.lower())

    # u at beginning of the word
    if word[0] == "u":
        # second char is a vowel
        if word[1] in VOWELS:
            word[0] = "v"

    # u in word
    for char in word:
        char_index = word.index(char)
        # vowel preceeds u and vowel follows
        if char == "u" and word[char_index - 1] in VOWELS and word[char_index + 1] in VOWELS:
            word[char_index] = "v"
        # consonant + u + u + vowel
        elif char == "u" and word[char_index -1] not in VOWELS and word[char_index + 1] == "u" and word[char_index + 2] in VOWELS:
            word[char_index + 1] = "v"

    return "".join(word)

if __name__ == "__main__":
    tests = ["amaui", "amatus", "auctor", "habui", "habuerit", "imbuantur", "fluuius", "exuuiae", "uita", "uae", "mortuus", "perpetuum"]

    for test in tests:
        print(convert_u_to_v(test))