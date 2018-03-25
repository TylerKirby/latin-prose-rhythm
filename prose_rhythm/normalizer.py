# -*- coding: utf-8 -*-
"""
Normalize Latin text for preprocessing.

The module assume that the text is already macronized and is utf 8 encoded.
"""
import regex as re
import json
import os

from cltk.prosody.latin.Syllabifier import Syllabifier

DEFAULT_PUNC = [".", "?", "!", ";", ":"]
DEFAULT_ABBREV = ["Agr.", "Ap.", "A.", "K.", "D.", "F.", "C.",
                  "Cn.", "L.", "Mam.", "M\'", "M.", "N.", "Oct.",
                  "Opet.", "Post.", "Pro.", "P.", "Q.", "Sert.",
                  "Ser.", "Sex.", "S.", "St.", "Ti.", "T.", "V.",
                  "Vol.", "Vop.", "Pl."]

class Normalizer(object):
    """
    Normalizes Latin text for preprocessing module.
    """

    def __init__(self, text, punctuation=None, replace_abbrev=True, abbrev=None):
        self.text = text
        self.punctuation = DEFAULT_PUNC if punctuation is None else punctuation
        self.replace_abbrev = replace_abbrev
        self.abbrev = DEFAULT_ABBREV if abbrev is None else abbrev

    def _replace_abbreviations(self):
        """
        Replace abbreviations
        :return:
        """
        for abbrev in self.abbrev:
            self.text = self.text.replace(abbrev, "abbrev")
        return self.text

    def _replace_roman_numerals(self):
        self.text = re.sub(r"(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?V|V?I{1,3}))",
                             "roman_numeral", self.text)
        return self.text

    def _remove_extra_white_space(self):
        self.text = re.sub(r"\s{2,}", " ", self.text)
        self.text = re.sub(r"^\s", "", self.text)
        return self.text

    @staticmethod
    def syllabify(word):
        syllable_data_path = os.path.join(os.path.dirname(__file__), 'syllables.json')
        with open(syllable_data_path) as file:
            syllable_data = json.load(file)
        if word in list(syllable_data.keys()):
            return syllable_data[word]
        else:
            return Syllabifier().syllabify(word)

    def normalize(self):
        """
        Normalize text.
        Punctuation is standardized with the supplied punctuation list.
        :return: normalized text
        """
        default_seperator = "."

        for punc in self.punctuation:
            self.text = self.text.replace(punc, default_seperator)

        if self.replace_abbrev:
            self.text = self._replace_abbreviations()

        self.text = self._replace_roman_numerals()
        self.text = self.text.lower()
        self.text = self._remove_extra_white_space()
        return self.text

if __name__ == "__main__":
    print(Normalizer("test").syllabify("fuit"))