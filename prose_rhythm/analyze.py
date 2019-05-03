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
        abbrev_excluded = 0
        bracket_excluded = 0
        short_clausulae = 0
        other_excluded = 0
        for sentence in tokens['text']:
            sentence_clausula = []
            syllable_count = sum([word['syllables_count'] for word in sentence['structured_sentence']])
            if not sentence['contains_abbrev'] and not sentence['contains_bracket_text'] and syllable_count > 3 and not sentence['contains_greek']:
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
                if sentence['contains_abbrev']:
                    abbrev_excluded += 1
                elif sentence['contains_bracket_text']:
                    bracket_excluded += 1
                elif syllable_count > 0 and syllable_count < 4:
                    short_clausulae += 1
                else:
                    other_excluded += 1
            sentence_clausula = sentence_clausula[::-1]
            sentence_clausula.append('x')
            if include_sentence:
                clausulae.append((sentence['plain_text_sentence'], ''.join(sentence_clausula)))
            else:
                clausulae.append(''.join(sentence_clausula))
        clausulae = clausulae[:-1]
        clausulae.append(sum([abbrev_excluded, bracket_excluded, short_clausulae, other_excluded])-1)
        clausulae.append(abbrev_excluded)
        clausulae.append(bracket_excluded)
        clausulae.append(short_clausulae)
        clausulae.append(other_excluded)
        return clausulae

    def rhythm_frequency(self, rhythms):
        """
        Return total number of rhythms, excluded clausulae, and counts of each rhythm type.
        :param rhythms: output of get_rhythms(tokens, include_sentence=False)
        :return: dict of stats
        """
        rhythm_tokens = rhythms[:-5]
        rhythm_count = dict(Counter(rhythm_tokens).most_common())
        rhythm_count.pop('x', None)
        rhythm_count['total_clausulae'] = len(rhythm_tokens)
        rhythm_count['total_excluded'] = rhythms[-5]
        if rhythm_count['total_excluded'] == -1:
            rhythm_count['total_excluded'] = 0
        rhythm_count['abbrev_excluded'] = rhythms[-4]
        rhythm_count['bracket_excluded'] = rhythms[-3]
        rhythm_count['short_excluded'] = rhythms[-2]
        rhythm_count['other_excluded'] = rhythms[-1]
        return rhythm_count


if __name__ == '__main__':
    text = """οὔ τοι ἀπόβλητ' ἐστὶ θεῶν ἐρικυδέα δῶρα, ὅσσα κεν αὐτοὶ δῶσιν, ἑκὼν δ' οὐκ ἄν τις ἕλοιτο. """
    p = Preprocessor(text=text)
    a = Analyze()
    tokens = p.tokenize()
    r = a.get_rhythms(tokens, include_sentence=False)
    print(a.rhythm_frequency(r))