# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""

from prose_rhythm.preprocessor import Preprocessor
import pprint

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

    def add_to_empty_tree(self, tree, new_node):
        for k, v in tree.items():
            if isinstance(v, list) and len(v) == 0:
                v.append(new_node)
                return tree
            elif isinstance(v, list) and len(v) != 0:
                return self.add_to_empty_tree(v, new_node)


    def make_rhythm_tree(self, rhythms):
        tokens = [token[::-1] for token in rhythms]
        height = max(len(token) for token in tokens)
        number_of_nodes = (2 ** height) - 1
        number_of_iter = len(tokens)

        tree = {"syllable_quantity": "x", "frequency": len(tokens), "probability": 100, "children": {}}

        for index, token in enumerate(tokens):
            if index == 0:
                for index, char in enumerate(token[1:]):
                    tree["children"][char] = 1

        return tree



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
    test_rhythms1 = ["-u-x", "--ux", "uu-x"]
    test_rhythms2 = ["u-u--u-x", "-uu---ux", "u-u-uu-x"]
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(Analyze().make_rhythm_tree(test_rhythms1))
