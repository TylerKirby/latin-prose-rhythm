# -*- coding: utf-8 -*-
'''
Process normalized Latin text into an annotated data set of prosimetric information.
'''

import regex as re

from cltk.prosody.latin.Syllabifier import Syllabifier
from prose_rhythm.normalizer import Normalizer

class Preprocessor(object):

    SHORT_VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']
    LONG_VOWELS = ['ā', 'ē', 'ī', 'ō', 'ū']
    VOWELS = SHORT_VOWELS + LONG_VOWELS
    DIPHTHONGS = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']

    SINGLE_CONSONANTS = ['b', 'c', 'd', 'g', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'f', 'j']
    DOUBLE_CONSONANTS = ['x', 'z']
    CONSONANTS = SINGLE_CONSONANTS + DOUBLE_CONSONANTS
    DIGRAPHS = ['ch', 'ph', 'th', 'qu']
    LIQUIDS = ['r', 'l']
    MUTES = ['b', 'p', 'd', 't', 'g', 'c']
    NASALS = ['m', 'n']
    SESTS = ['sc', 'sm', 'sp', 'st', 'z']

    ABBREV = ['Agr.', 'Ap.', 'A.', 'K.', 'D.', 'F.', 'C.',
                       'Cn.', 'L.', 'Mam.', 'M\'', 'M.', 'N.', 'Oct.',
                       'Opet.', 'Post.', 'Pro.', 'P.', 'Q.', 'Sert.',
                       'Ser.', 'Sex.', 'S.', 'St.', 'Ti.', 'T.', 'V.',
                       'Vol.', 'Vop.', 'Pl.']

    def __init__(self, text, punctuation=['.', '?', '!', ';', ':'], title='No Title'):
        self.text = text
        self.punctuation = punctuation
        self.title = title

    def _tokenize_syllables(self, word):
        '''
        Tokenize syllables for word.
        'mihi' -> [{'syllable': 'mi', index: 0, ... } ... ]
        Syllable properties:
            syllable: string -> syllable
            index: int -> postion in word
            long_by_nature: bool -> is syllable long by nature
            accented: bool -> does receive accent
            long_by_position: bool -> is syllable long by position
        :param word: string
        :return: list
        '''
        syllable_tokens = []
        syllables = Syllabifier().syllabify(word)

        longs = self.LONG_VOWELS + self.DIPHTHONGS

        for i in range(0, len(syllables)):
            # basic properties
            syllable_dict = {'syllable': syllables[i], 'index': i, 'elide': (False, None)}

            # is long by nature
            syllable_dict['long_by_nature'] = True if any(long in syllables[i] for long in longs) else False

            # long by position intra word
            if i < len(syllables) - 1 and syllable_dict['syllable'][-1] in self.CONSONANTS:
                if syllable_dict['syllable'][-1] in self.DOUBLE_CONSONANTS or syllables[i + 1][0] in self.CONSONANTS:
                    syllable_dict['long_by_position'] = (True, None)
                else:
                    syllable_dict['long_by_position'] = (False, None)
            elif i < len(syllables) - 1 and syllable_dict['syllable'][-1] in self.VOWELS and len(syllables[i + 1]) > 1:
                if syllables[i + 1][0] in self.MUTES and syllables[i + 1][1] in self.LIQUIDS:
                    syllable_dict['long_by_position'] = (False, 'mute+liquid')
                elif syllables[i + 1][0] in self.CONSONANTS and syllables[i + 1][1] in self.CONSONANTS or syllables[i + 1][0] in self.DOUBLE_CONSONANTS:
                    syllable_dict['long_by_position'] = (True, None)
                else:
                    syllable_dict['long_by_position'] = (False, None)
            else:
                syllable_dict['long_by_position'] = (False, None)

            syllable_tokens.append(syllable_dict)

            # is accented
            if len(syllables) > 2 and i == len(syllables) - 2:
                if syllable_dict['long_by_nature'] or syllable_dict['long_by_position'][0]:
                    syllable_dict['accented'] = True
                else:
                    syllable_tokens[i - 1]['accented'] = True
            elif len(syllables) == 2 and i == 0 or len(syllables) == 1:
                syllable_dict['accented'] = True

            syllable_dict['accented'] = False if 'accented' not in syllable_dict else True

        return syllable_tokens

    def _tokenize_words(self, sentence):
        '''
        Tokenize words for sentence.
        'Puella bona est' -> [{word: puella, index: 0, ... }, ... ]
        Word properties:
            word: string -> word
            index: int -> position in sentence
            syllables: list -> list of syllable objects
            syllables_count: int -> number of syllables in word
        :param sentence: string
        :return: list
        '''
        tokens = []
        split_sent = sentence.split(' ')
        for i in range(0, len(split_sent)):
            # basic properties
            word_dict = {'word': split_sent[i], 'index': i}

            # syllables and syllables count
            word_dict['syllables'] = self._tokenize_syllables(split_sent[i])
            word_dict['syllables_count'] = len(word_dict['syllables'])

            # is elidable
            if i != 0 and word_dict['syllables'][0]['syllable'][0] in self.VOWELS or i != 0 and word_dict['syllables'][0]['syllable'][0] == 'h':
                last_syll_prev_word = tokens[i - 1]['syllables'][-1]
                if last_syll_prev_word['syllable'][-1] in self.SHORT_VOWELS:
                    last_syll_prev_word['elide'] = (True, 'weak')
                elif last_syll_prev_word['syllable'][-1] in self.LONG_VOWELS and self.DIPHTHONGS or last_syll_prev_word['syllable'][-1] == 'm':
                    last_syll_prev_word['elide'] = (True, 'strong')

            # long by position inter word
            if i > 0 and tokens[i - 1]['syllables'][-1]['syllable'][-1] in self.CONSONANTS and word_dict['syllables'][0]['syllable'][0] in self.CONSONANTS:
                # previous word ends in consonant and current word begins with consonant
                tokens[i - 1]['syllables'][-1]['long_by_position'] = (True, None)
            elif i > 0 and tokens[i - 1]['syllables'][-1]['syllable'][-1] in self.VOWELS and word_dict['syllables'][0]['syllable'][0] in self.CONSONANTS:
                # previous word ends in vowel and current word begins in consonant
                if any(sest in word_dict['syllables'][0]['syllable'] for sest in self.SESTS):
                    # current word begins with sest
                    tokens[i - 1]['syllables'][-1]['long_by_position'] = (False, 'sest')
                elif word_dict['syllables'][0]['syllable'][0] in self.MUTES and word_dict['syllables'][0]['syllable'][1] in self.LIQUIDS:
                    # current word begins with mute + liquid
                    tokens[i - 1]['syllables'][-1]['long_by_position'] = (False, 'mute+liquid')
                elif word_dict['syllables'][0]['syllable'][0] in self.DOUBLE_CONSONANTS or word_dict['syllables'][0]['syllable'][1] in self.CONSONANTS:
                    # current word begins 2 consonants
                    tokens[i - 1]['syllables'][-1]['long_by_position'] = (True, None)


            tokens.append(word_dict)

        return tokens

    def tokenize(self):
        '''
        Tokenize text on supplied characters.
        'Puella bona est. Puer malus est.' -> [ [{word: puella, syllables: [...], index: 0}, ... ], ... ]
        :return:list
        '''
        normalized_text = Normalizer(self.text).normalize()
        default_punc = "."
        tokenized_sentences = [sentence.strip() for sentence in normalized_text.split(default_punc) if sentence.strip() is not '']

        tokenized_text = []
        for sentence in tokenized_sentences:
            sentence_dict = {}
            sentence_dict['contains_abbrev'] = True if 'abbrev' in sentence else False
            sentence = re.sub(r'\sabbrev\s', ' ', sentence)
            sentence_dict['plain_text_sentence'] = sentence
            sentence_dict['structured_sentence'] = self._tokenize_words(sentence)
            tokenized_text.append(sentence_dict)

        return {'title': self.title, 'text': tokenized_text}


if __name__ == '__main__':
    test_text = "Galliā est omnīs dīvīsa in partēs trēs quārum ūnam incolunt Belgae aliam Aquītānī tertiam quī ipsōrum " \
                "lingua Celtae nostra Gallī appellantur. hī omnēs linguā īnstitūtīs lēgibus inter sē differunt. Gallōs" \
                " ab Aquītānīs Garunna flūmen ā Belgīs Matrona et Sēquana dīvidit. hōrum omnium fortissimī sunt Belgae " \
                "proptereā quod ā cultū atque hūmānitāte prōvinciae longissimē absunt minimēque ad eōs mercātōrēs " \
                "saepe commeant atque ea quae ad effēminandōs animōs pertinent important proximīque sunt Germānīs " \
                "quī trāns Rhēnum incolunt quibuscum continenter bellum gerunt. quā dē causā Helvētiī quoque reliquōs" \
                " Gallōs virtūte praecēdunt quod ferē cotīdiānīs proeliīs cum Germānīs contendunt cum aut suīs fīnibus" \
                " eōs prohibent aut ipsī in eōrum fīnibus bellum gerunt. eōrum ūna pars quam Gallōs obtinēre dictum est" \
                " initium capit ā flūmine Rhodanō continētur Garunna flūmine Ōceanō fīnibus Belgārum attingit etiam " \
                "ab Sēquanīs et Helvētiīs flūmen Rhēnum vergit ad  septentriōnēs. Belgae ab extrēmīs Galliae" \
                " fīnibus oriuntur pertinent ad īnferiōrem partem flūminis Rhēnī spectant in septentriōnem et" \
                " orientem sōlem."
    test_sentences = test_text.split('.')
    print(Preprocessor(test_text).tokenize())
