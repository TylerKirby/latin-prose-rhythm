# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""


class Analyze(object):
    """
    Analyze Latin prose rhythms.
    """

    def __init__(self, clausula_length=8):
        self.clausula_length = clausula_length

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
            sentence_clausula = ''
            if not sentence['contains_numeral'] and not sentence['contains_abbrev']:
                for word in reversed(sentence['structured_sentence']):
                    for syllable in reversed(word['syllables']):
                        if len(sentence_clausula) < self.clausula_length:
                            if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                                sentence_clausula = '-' + sentence_clausula
                            elif syllable['elide']:
                                pass
                            else:
                                sentence_clausula = 'u' + sentence_clausula
                sentence_clausula = sentence_clausula[:-1] + 'x'
                clausulae.append((sentence['plain_text_sentence'], sentence_clausula))

        return clausulae


if __name__ == "__main__":
    pass
