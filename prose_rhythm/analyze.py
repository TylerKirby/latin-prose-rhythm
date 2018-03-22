# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""

from prose_rhythm.preprocessor import Preprocessor

class Analyze(object):
    """
    Analyze Latin prose rhythms.
    """

    def __init__(self, tokens):
        self.tokens = tokens

    def get_rhythms(self, clausulae_length=8, include_short_clausula=True):
        """
        Return a flat list of rhythms.
        Desired clausula length is passed as a parameter. Clausula shorter than the specified
        length can be exluded.
        :return:
        """
        clausulae = []
        for sentence in self.tokens['text']:
            sentence_clausula = ''
            for word in reversed(sentence['structured_sentence']):
                for syllable in reversed(word['syllables']):
                    if len(sentence_clausula) < clausulae_length:
                        if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                            sentence_clausula = '-' + sentence_clausula
                        else:
                            sentence_clausula = 'u' + sentence_clausula
            sentence_clausula = sentence_clausula[:-1] + 'x'
            clausulae.append(sentence_clausula)
        return clausulae




if __name__ == "__main__":
    pass
