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

    def __init__(self, clausula_length=8, include_short_clausula=True):
        self.clausula_length = clausula_length
        self.include_short_clausula = include_short_clausula

    # TODO: Ignore rhythms with abbrev and roman numerals
    def get_rhythms(self, tokens):
        """
        Return a flat list of rhythms.
        Desired clausula length is passed as a parameter. Clausula shorter than the specified
        length can be exluded.
        :return:
        """
        clausulae = []
        for sentence in tokens['text']:
            sentence_clausula = ''
            for word in reversed(sentence['structured_sentence']):
                for syllable in reversed(word['syllables']):
                    if len(sentence_clausula) < self.clausula_length:
                        if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                            sentence_clausula = '-' + sentence_clausula
                        else:
                            sentence_clausula = 'u' + sentence_clausula
            sentence_clausula = sentence_clausula[:-1] + 'x'
            clausulae.append(sentence_clausula)

        if not self.include_short_clausula:
            return [clausula for clausula in clausulae if len(clausula) == self.clausula_length]

        return clausulae


    def rhythm_dict(self, rhythms):
        total_rhythms = len(rhythms)
        print(total_rhythms)
        root = "x"

        rhythm_dict = { i:[] for i in range(1, len(rhythms[0]))}
        for rhythm in rhythms:
            rhythm = rhythm[:-1]
            for key, char in enumerate(rhythm):
                key += 1
                rhythm_dict[key].append(char)

        for key, temp_rhythms in rhythm_dict.items():
            long_count = temp_rhythms.count("-")
            percent_long = long_count / total_rhythms
            rhythm_dict[key] = format(percent_long, '.2f')

        return rhythm_dict


if __name__ == "__main__":
    test_rhythms = ["-u-u--ux", "--u--u-x", "-u-u-u-x"]
    print(Analyze().rhythm_dict(test_rhythms))
