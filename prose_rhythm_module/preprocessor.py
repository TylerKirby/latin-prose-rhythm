"""
Preprocessor
"""

import regex as re

from cltk.stem.latin.syllabifier import Syllabifier

class Preprocessor(object):

    SHORT_VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']
    LONG_VOWELS = ['ā', 'ē', 'ī', 'ō', 'ū']
    VOWELS = SHORT_VOWELS + LONG_VOWELS
    DIPHTHONGS = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']

    SINGLE_CONSONANTS = ['b', 'c', 'd', 'g', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'f', 'j']
    DOUBLE_CONSONANTS = ['x', 'z']
    CONSONANTS = SINGLE_CONSONANTS + DOUBLE_CONSONANTS
    DIGRAPHS = ['ch', 'ph', 'th', 'qu']
    LIQUIDS = ['r', 'l']

    def __init__(self, text, punctuation=['.']):
        self.text = text
        self.punctuation = punctuation


    def _u_to_v(self, word):
        """
        Convert u in word to v.
        :param word: string
        :return: string
        """
        word = list(word.lower())

        # u at beginning of the word
        if word[0] == "u" and word[1] in self.VOWELS and word[1] != "u":
            word[0] = "v"
        elif word[0] == "u" and word[1] == "u" and word[2] not in self.VOWELS:
            word[0] = "v"
        elif word[0] == "u" and word[1] == "u" and word[2] in self.VOWELS:
            word[1] = "v"

        # u in word
        for char in word:
            char_index = word.index(char)
            if char_index != len(word) - 1 and char == "u":
                # consonant + u + vowel (that's not i)
                if word[char_index - 1] not in self.VOWELS and word[char_index + 1] in self.VOWELS and word[
                            char_index + 1] != "u" and word[char_index + 1] != "i" and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index] = "v"
                # vowel preceeds u and vowel follows
                if len(word) > 2 and word[char_index - 1] in self.VOWELS and word[char_index + 1] in self.VOWELS and word[char_index + 1] != "u":
                    word[char_index] = "v"
                # consonant + u + u + vowel
                if len(word) > 3 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == "u" and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index + 1] = "v"
                # consonant + u + i + consonant
                if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == "i" and word[
                            char_index + 2] not in self.VOWELS:
                    word[char_index] = "v"
                # i + u + u + vowel
                if len(word) > 3 and word[char_index - 1] == "i" and word[char_index + 1] == "u" and word[char_index + 2] in self.VOWELS:
                    word[char_index + 1] = "v"
        return "".join(word)

    def _i_to_j(self, word):
        """
        Convert i in word to j.
        :param word: string
        :return: string
        """
        PREFIXES = ["ab", "ad", "ante", "circum", "cum", "in", "inter", "ob", "per", "praeter", "sub", "subter", "super", "con"]

        word_prefix = [prefix for prefix in PREFIXES if word.startswith(prefix)]
        word_prefix_end_index = len(word_prefix[0]) if len(word_prefix) == 1 else None

        word = list(word.lower())

        # i at the beginning of a word
        if word[0] == "i" and word[1] in self.VOWELS:
            word[0] = "j"

        # word has prefix
        if word_prefix_end_index != None and word[word_prefix_end_index] == "i":
            # prefix + i + vowel
            if word[word_prefix_end_index + 1] in self.VOWELS:
                word[word_prefix_end_index] = "j"
            #prefix + i + consonant
            else:
                word.insert(word_prefix_end_index, "j")

        return "".join(word)

    def _i_u_to_j_v(self):
        """
        Convert all u's and i's to v's and j's.
        Note that u to v converter must be used before i to j converter.
        :return:
        """
        converted_text = []
        for word in self.text.split(" "):
            converted_word = self._i_to_j(self._u_to_v(word))
            converted_text.append(converted_word)
        return " ".join(converted_text)

    def _tokenize_syllables(self, word):
        """
        Tokenize syllables for word.
        "mihi" -> [{"syllable": "mi", index: 0, ... } ... ]
        Syllable properties:
            syllable: string -> syllable
            index: int -> postion in word
            long_by_nature: bool -> is syllable long by nature
            accented: bool -> does receive accent
            long_by_position: bool -> is syllable long by position
        :param word: string
        :return: list
        """
        syllable_tokens = []
        syllables = Syllabifier().syllabify(word)

        longs = self.LONG_VOWELS + self.DIPHTHONGS

        for i in range(0, len(syllables)):
            # basic properties
            syllable_dict = {"syllable": syllables[i], "index": i}

            # is long by nature
            syllable_dict["long_by_nature"] = True if any(long in syllables[i] for long in longs) else False

            # is accented
            if len(syllables) > 2 and i == len(syllables) - 2:
                if syllable_dict["long_by_nature"]:
                    syllable_dict["accented"] = True
                else:
                    syllable_tokens[i - 1]["accented"] = True
            elif len(syllables) == 2 and i == 0 or len(syllables) == 1:
                syllable_dict["accented"] = True

            syllable_dict["accented"] = False if "accented" not in syllable_dict else True

            # long by position intra word
            if i > 0 and i > len(syllables) - 1 and syllable_dict["syllable"][-1] in self.CONSONANTS:
                if syllable_dict["syllable"][-1] in self.DOUBLE_CONSONANTS:
                    syllable_dict["long_by_position"] = True
                elif syllables[i + 1][0] in self.CONSONANTS:
                    syllable_dict["long_by_position"] = True
            else:
                syllable_dict["long_by_position"] = False

            syllable_tokens.append(syllable_dict)

        return syllable_tokens

    def _tokenize_words(self, sentence):
        """
        Tokenize words for sentence.
        "Puella bona est" -> [{word: puella, index: 0, ... }, ... ]
        Word properties:
            word: string -> word
            index: int -> position in sentence
            syllables: list -> list of syllable objects
            syllables_count: int -> number of syllables in word
        :param sentence: string
        :return: list
        """
        tokens = []
        split_sent = sentence.split(" ")
        for i in range(0, len(split_sent)):
            # basic properties
            word_dict = {"word": split_sent[i], "index": i}

            # syllables and syllables count
            word_dict["syllables"] = self._tokenize_syllables(split_sent[i])
            word_dict["syllables_count"] = len(word_dict["syllables"])

            # is elidable
            if i != 0 and word_dict["syllables"][0]["syllable"][0] in self.VOWELS:
                last_syll_prev_word = tokens[i - 1]["syllables"][-1]
                if last_syll_prev_word["syllable"][-1] in self.SHORT_VOWELS:
                    last_syll_prev_word["elide"] = (True, "weak")
                elif last_syll_prev_word["syllable"][-1] in self.LONG_VOWELS and self.DIPHTHONGS or last_syll_prev_word["syllable"][-1] == "m":
                    last_syll_prev_word["elide"] = (True, "strong")

            # long by position inter word
            if i > 0 and tokens[i - 1]["syllables"][-1]["syllable"][-1] in self.CONSONANTS and word_dict["syllables"][0]["syllable"][0] in self.CONSONANTS:
                tokens[i - 1]["syllables"][-1]["long_by_position"] = True


            tokens.append(word_dict)

        return tokens

    def tokenize(self):
        """
        Tokenize text on supplied characters.
        "Puella bona est. Puer malus est." -> [ [{word: puella, syllables: [...], index: 0}, ... ], ... ]
        :return:list
        """
        # tokenize text on supplied punc
        default_seperator = '.'
        for punc in self.punctuation:
            self.text = self.text.replace(punc, default_seperator)

        # regex remove all non-alphanumeric chars except '.' and ' ', then convert i/u to j/v
        clean_text = re.sub(r"[^a-z.\s]", "", self._i_u_to_j_v())
        tokenized_sentences = [sentence.strip() for sentence in clean_text.split(default_seperator) if sentence.strip() is not '']

        return [self._tokenize_words(sentence) for sentence in tokenized_sentences]


if __name__ == "__main__":
    test_text = "Mihi coniciō iui it, quam optāram, auditū dedērunt: te miror, Antōnī, quorum. Iuuēnum iuuō coniectus et si cetera; coniugo auctor uiā uector."
    test_class = Preprocessor(test_text, ['.', ';'])
    print(test_class._tokenize_syllables("conjiciō"))
