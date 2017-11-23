"""
Preprocessor
"""

from cltk.stem.latin.syllabifier import Syllabifier

class Preprocessor(object):

    VOWELS = ['ā', 'ē', 'ī', 'ō', 'ū', 'ȳ','a', 'e', 'i', 'o', 'u', 'y']

    def __init__(self, text, punctuation):
        self.text = text
        self.punctuation = punctuation


    def u_to_v(self, word):
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
                            char_index + 1] is not "u" and word[char_index + 1] is not "i" and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index] = "v"
                # vowel preceeds u and vowel follows
                if len(word) > 2 and word[char_index - 1] in self.VOWELS and word[char_index + 1] in self.VOWELS and word[char_index - 1] != "i":
                    word[char_index] = "v"
                # consonant + u + u + vowel
                if len(word) > 3 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == "u" and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index + 1] = "v"
                # consonant + u + i + consonant
                if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == "i" and word[
                            char_index + 2] not in self.VOWELS:
                    word[char_index] = "v"
                # consonantal i at start of word
                if len(word) > 3 and word[0] == "i" and word[char_index + 1] == "u":
                    word[char_index + 1] = "v"
        return "".join(word)

    def preprocessed_text(self):
        """
        Tokenize text on supplied characters.
        :return: tokenized text
        :rtype : list
        """
        default_seperator = self.punctuation[0]
        for punc in self.punctuation[1:]:
            self.text = self.text.replace(punc, default_seperator)
        return [sentence.strip() for sentence in self.text.split(default_seperator) if sentence.strip() is not '']

    def syllabified(self):
        """
        Syllabify text.
        :return: syllabified text
        :rtype : list
        """
        preprocessed_text = self.preprocessed_text()
        syllabifier = Syllabifier()
        syllabified_sentence = []
        for sentence in preprocessed_text:
            syllabified_words = [syllabifier.syllabify(word) for word in sentence.lower().split(' ') if '[' not in word]
            syllabified_sentence.append(syllabified_words)
        syllabified = [sentence for sentence in syllabified_sentence if [] not in sentence]
        return syllabified

if __name__ == "__main__":
    print(Preprocessor("test", ['.']).u_to_v("iuuenum"))