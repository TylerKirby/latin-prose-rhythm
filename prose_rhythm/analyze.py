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

    def __init__(self, clausula_length=8):
        self.clausula_length = clausula_length

    @staticmethod
    def filter_elided_syllables(flat_syllable_list):
        i = 0
        while i < len(flat_syllable_list):
            if flat_syllable_list[i]['elide'][0]:
                del flat_syllable_list[i+1]
            i += 1
        return flat_syllable_list

    def process_syllables(self, flat_syllable_list):
        """
        Return flat list of syllables with final syllable
        removed and list reversed. Elided syllables
        are removed as well
        """
        flat_syllable_list = self.filter_elided_syllables(flat_syllable_list)[:-1]
        return flat_syllable_list[::-1]

    # TODO Rewrite to account for elision
    def get_rhythms(self, tokens):
        """
        Return a flat list of rhythms.
        Desired clausula length is passed as a parameter. Clausula shorter than the specified
        length can be exluded.
        :return:
        """
        clausulae = []
        for sentence in tokens['text']:
            sentence_clausula = []
            if not sentence['contains_numeral'] and not sentence['contains_abbrev']:
                syllables = [word['syllables'] for word in sentence['structured_sentence']]
                flat_syllables = [syllable for word in syllables for syllable in word]
                flat_syllables = self.process_syllables(flat_syllables)
                for syllable in flat_syllables:
                    if len(sentence_clausula) < self.clausula_length:
                        if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                            sentence_clausula.append('-')
                        else:
                            sentence_clausula.append('u')
            sentence_clausula = sentence_clausula[::-1]
            sentence_clausula.append('x')
            clausulae.append((sentence['plain_text_sentence'], ''.join(sentence_clausula)))
        return clausulae[:-1]


if __name__ == "__main__":
    not_elided = "multitūdinis auctōritāte pūblicā armāre."
    preprocessor = Preprocessor(text=not_elided)
    analysis = Analyze()
    tokens = preprocessor.tokenize()
    print(analysis.get_rhythms(tokens))
\