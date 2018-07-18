# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""
from preprocessor import Preprocessor


class Analyze(object):
    """
    Analyze Latin prose rhythms.
    """

    def __init__(self, clausula_length=8):
        self.clausula_length = clausula_length

    @staticmethod
    def filter_elided_syllables(flat_syllable_list):
        i = 0
        for i in range(0, len(flat_syllable_list) - 1):
            if flat_syllable_list[i]['elide'][0]:
                flat_syllable_list.pop(i+1)
        return flat_syllable_list

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
                filtered_elided = self.filter_elided_syllables(flat_syllables)
                for syllable in filtered_elided[::-1][:-1]:
                    if len(sentence_clausula) < self.clausula_length:
                        if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                            sentence_clausula.append('-')
                        else:
                            sentence_clausula.append('u')
            sentence_clausula.append('x')
            clausulae.append((sentence['plain_text_sentence'], ''.join(sentence_clausula)))
        return clausulae


if __name__ == "__main__":
    not_elided = "sī quem habētis dēpōnite. sī quem habētis dēpōnite."
    preprocessor = Preprocessor(text=not_elided)
    analysis = Analyze()
    tokens = preprocessor.tokenize()
    print(analysis.get_rhythms(tokens))
