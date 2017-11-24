"""
Module for analyzing the prose rhythm of Latin texts.
"""

from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stem.latin.j_v import JVReplacer

# TODO: Check for elision
# TODO: Rewrite preprocessing to remove numbers and punc not in self.punc


class Prose_Rhythm_Scanner(object):

    SESTS = ['sc', 'sm', 'sp', 'st', 'z']
    MUTES = ['b', 'c', 'k', 'd', 'g', 'p', 't']
    DIGRAPHS = ['ch', 'ph', 'th', 'qu']
    LIQUIDS = ['r', 'l']
    VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']
    SINGLE_CONSONANTS = ['b', 'c', 'd', 'g', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'f', 'j']
    DOUBLE_CONSONANTS = ['x', 'z']
    LONG_VOWELS = ['ā', 'ē', 'ī', 'ō', 'ū']
    DIPHTHONGS = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']
    NASALS = ['m', 'n']

    def __init__(self, elision, sests, mute_plus_liquid, punctuation, text):
        self.elision = elision
        self.sests = sests
        self.mute_plus_liquid  = mute_plus_liquid
        self.punctuation = punctuation
        self.text = text

    def long_by_nature(self, syllable):
        """
        Check if syllable is long by nature.
        :return: true if long by nature
        :rtype : boolean
        """
        for vowel in self.LONG_VOWELS:
            if vowel in syllable:
                return True
        for diphthong in self.DIPHTHONGS:
            if diphthong in syllable:
                return True
        return False

if __name__ == "__main__":
    pass