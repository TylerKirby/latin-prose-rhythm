# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""

from prose_rhythm.preprocessor import Preprocessor
from collections import Counter


class Analyze(object):
    """
    Analyze Latin prose rhythms.
    """

    def __init__(self, clausula_length=13):
        self.clausula_length = clausula_length

    def process_syllables(self, flat_syllable_list):
        """
        Return flat list of syllables with final syllable
        removed and list reversed. Elided syllables
        are removed as well
        """
        remove_elided = [syll for syll in flat_syllable_list if not syll['elide'][0]]
        processed_sylls = remove_elided[:-1]
        return processed_sylls[::-1]

    def get_rhythms(self, tokens, include_sentence=True):
        """
        Return a flat list of rhythms.
        Desired clausula length is passed as a parameter. Clausula shorter than the specified
        length can be exluded.
        :return:
        """
        clausulae = []
        excluded = 0
        abbrev_excluded = 0
        bracket_excluded = 0
        for sentence in tokens['text']:
            sentence_clausula = []
            if not sentence['contains_abbrev'] and not sentence['contains_bracket_text']:
                syllables = [word['syllables'] for word in sentence['structured_sentence']]
                flat_syllables = [syllable for word in syllables for syllable in word]
                flat_syllables = self.process_syllables(flat_syllables)
                for syllable in flat_syllables:
                    if len(sentence_clausula) < self.clausula_length - 1:
                        if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                            sentence_clausula.append('-')
                        else:
                            sentence_clausula.append('u')
            else:
                excluded += 1
                if sentence['contains_abbrev']:
                    abbrev_excluded += 1
                if sentence['contains_bracket_text']:
                    bracket_excluded += 1
            sentence_clausula = sentence_clausula[::-1]
            sentence_clausula.append('x')
            if include_sentence:
                clausulae.append((sentence['plain_text_sentence'], ''.join(sentence_clausula)))
            else:
                clausulae.append(''.join(sentence_clausula))
        clausulae = clausulae[:-1]
        clausulae.append(excluded)
        clausulae.append(abbrev_excluded)
        clausulae.append(bracket_excluded)
        return clausulae

    def rhythm_frequency(self, rhythms):
        """
        Return total number of rhythms, excluded clausulae, and counts of each rhythm type.
        :param rhythms: output of get_rhythms(tokens, include_sentence=False)
        :return: dict of stats
        """
        rhythm_tokens = rhythms[:-3]
        rhythm_count = dict(Counter(rhythm_tokens).most_common())
        rhythm_count.pop('x', None)
        rhythm_count['total_clausulae'] = len(rhythm_tokens)
        rhythm_count['total_excluded'] = rhythms[-3]
        rhythm_count['abbrev_excluded'] = rhythms[-2]
        rhythm_count['bracket_excluded'] = rhythms[-1]
        return rhythm_count


if __name__ == '__main__':
    text = """et suō jūre possit?
sed praesidiō esse, ut intellegātis contrā hesternam illam 
contiōnem licēre vōbīs quod sentiātis līberē jūdicāre. """
    p = Preprocessor(text=text)
    a = Analyze()
    tokens = p.tokenize()
    r = a.get_rhythms(tokens, include_sentence=False)
    print(a.rhythm_frequency(r))