# - coding: utf-8 --
'''
Preprocessor
'''

import regex as re

from cltk.stem.latin.syllabifier import Syllabifier

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


    def _u_to_v(self, word):
        '''
        Convert u in word to v.
        :param word: string
        :return: string
        '''
        word = list(word.lower())

        # u at beginning of the word
        if word[0] == 'u' and word[1] in self.VOWELS and word[1] != 'u':
            word[0] = 'v'
        elif word[0] == 'u' and word[1] == 'u' and word[2] not in self.VOWELS:
            word[0] = 'v'
        elif word[0] == 'u' and word[1] == 'u' and word[2] in self.VOWELS:
            word[1] = 'v'

        # u in word
        for char in word:
            char_index = word.index(char)
            if char_index != len(word) - 1 and char == 'u':
                # consonant + u + vowel (that's not i)
                if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] in self.VOWELS and word[
                            char_index + 1] != 'u' and word[char_index + 1] != 'i' and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index] = 'v'
                # vowel preceeds u and vowel follows
                if len(word) > 2 and word[char_index - 1] in self.VOWELS and word[char_index + 1] in self.VOWELS and word[char_index + 1] != 'u':
                    word[char_index] = 'v'
                # consonant + u + u + vowel
                if len(word) > 3 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == 'u' and word[
                            char_index + 2] in self.VOWELS:
                    word[char_index + 1] = 'v'
                # consonant + u + i + consonant
                if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == 'i' and word[
                            char_index + 2] not in self.VOWELS:
                    word[char_index] = 'v'
                # i + u + u + vowel
                if len(word) > 3 and word[char_index - 1] == 'i' and word[char_index + 1] == 'u' and word[char_index + 2] in self.VOWELS:
                    word[char_index + 1] = 'v'
        return ''.join(word)

    def _i_to_j(self, word):
        '''
        Convert i in word to j.
        :param word: string
        :return: string
        '''
        PREFIXES = ['ab', 'ad', 'ante', 'circum', 'cum', 'in', 'inter', 'ob', 'per', 'praeter', 'sub', 'subter', 'super', 'con']

        word_prefix = [prefix for prefix in PREFIXES if word.startswith(prefix)]
        word_prefix_end_index = len(word_prefix[0]) if len(word_prefix) == 1 else None

        word = list(word.lower())

        # i at the beginning of a word
        if word[0] == 'i' and word[1] in self.VOWELS:
            word[0] = 'j'

        # word has prefix
        if word_prefix_end_index != None and word_prefix_end_index < len(word) - 1 and word[word_prefix_end_index] == 'i':
            # prefix + i + vowel
            if word[word_prefix_end_index + 1] in self.VOWELS:
                word[word_prefix_end_index] = 'j'
            #prefix + i + consonant
            else:
                word.insert(word_prefix_end_index, 'j')

        return ''.join(word)

    def _i_u_to_j_v(self):
        '''
        Convert all u's and i's to v's and j's.
        Note that u to v converter must be used before i to j converter.
        :return:
        '''
        converted_text = []
        for word in self.text.split(' '):
            converted_word = self._i_to_j(self._u_to_v(word))
            converted_text.append(converted_word)
        return ' '.join(converted_text)

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
        # tokenize text on supplied punc
        default_seperator = '.'

        for punc in self.punctuation:
            self.text = self.text.replace(punc, default_seperator)

        for abbrev in self.ABBREV:
            self.text = self.text.replace(abbrev, 'ABBREV')

        lower_text = self.text.lower()
        clean_text = re.sub(r'[^a-z.\sāēīōū]', '', lower_text)
        clean_text = re.sub(r'\s{2}', ' ', clean_text)

        tokenized_sentences = [sentence.strip() for sentence in clean_text.split(default_seperator) if sentence.strip() is not '']

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
    test_text = 'Galliā est omnīs dīvīsa in partēs trēs quārum ūnam incolunt Belgae aliam Aquītānī tertiam quī ipsōrum lingua Celtae nostra Gallī appellantur. hī omnēs linguā īnstitūtīs lēgibus inter sē differunt. Gallōs ab Aquītānīs Garunna flūmen ā Belgīs Matrona et Sēquana dīvidit. hōrum omnium fortissimī sunt Belgae proptereā quod ā cultū atque hūmānitāte prōvinciae longissimē absunt minimēque ad eōs mercātōrēs saepe commeant atque ea quae ad effēminandōs animōs pertinent important proximīque sunt Germānīs quī trāns Rhēnum incolunt quibuscum continenter bellum gerunt. quā dē causā Helvētiī quoque reliquōs Gallōs virtūte praecēdunt quod ferē cotīdiānīs proeliīs cum Germānīs contendunt cum aut suīs fīnibus eōs prohibent aut ipsī in eōrum fīnibus bellum gerunt. eōrum ūna pars quam Gallōs obtinēre dictum est initium capit ā flūmine Rhodanō continētur Garunna flūmine Ōceanō fīnibus Belgārum attingit etiam ab Sēquanīs et Helvētiīs flūmen Rhēnum vergit ad  septentriōnēs. Belgae ab extrēmīs Galliae fīnibus oriuntur pertinent ad īnferiōrem partem flūminis Rhēnī spectant in septentriōnem et orientem sōlem. Aquītānia ā Garunnā flūmine ad Pȳrēnaeōs montēs et eam partem Ōceanī quae est ad Hispāniam pertinet spectat inter occāsum sōlis et septentriōnēs. Apud Helvētiōs longē nōbilissimus fuit et dītissimus Orgetorix. is M. Messāla et P. M. Pīsōne cōnsulibus rēgnī cupiditāte inductus conjūrātiōnem nōbilitātis fēcit et cīvitātī persuāsit ut dē fīnibus suīs cum omnibus cōpiīs exīrent perfacile esse cum virtūte omnibus praestārent tōtīus Galliae imperiō potīrī. id hoc facilius iīs persuāsit quod undique locī nātūra Helvētiī continentur ūna ex parte flūmine Rhēnō lātissimō atque altissimō quī agrum Helvētium ā Germānīs dīvidit altera ex parte monte Jūrā altissimō quī est inter Sēquanōs et Helvētiōs tertia lacū Lemannō et flūmine Rhodanō quī prōvinciam nostram ab Helvētiīs dīvidit. hīs rēbus fīēbat ut et minus lātē vagārentur et minus facile fīnitimīs bellum īnferre possent quā ex parte hominēs bellandī cupidī magnō dolōre adficiēbantur. prō multitūdine autem hominum et prō glōriā bellī atque fortitūdinis angustōs sē fīnēs habēre arbitrābantur quī in longitūdinem mīlia passuum ccxl in lātitūdinem clxxx patēbant. Hīs rēbus adductī et auctōritāte Orgetorigis permōtī cōnstituērunt ea quae ad proficīscendum pertinērent comparāre jūmentōrum et carrōrum quam maximum numerum coemere sēmentēs quam maximās facere ut in itinere cōpia frūmentī suppeteret cum proximīs cīvitātibus pācem et amīcitiam cōnfirmāre. ad eās rēs cōnficiendās biennium sibi satis esse dūxērunt in  tertium annum profectiōnem lēge cōnfirmant. ad eās rēs cōnficiendās Orgetorix dēligitur. is sibi lēgātiōnem ad cīvitātēs suscēpit. in eō itinere persuādet Castīcō Catamantaloedis fīliō Sēquanō cūjus pater rēgnum in Sēquanīs multōs annōs obtinuerat et ab senātū populī Rōmānī amīcus appellātus erat ut rēgnum in cīvitāte suā occupāret quod pater ante habuerat itemque Dumnorigī Haeduō frātrī Dīviciācī quī eō tempore prīncipātum in cīvitāte obtinēbat ac maximē plēbī acceptus erat ut īdem cōnārētur persuādet eīque fīliam suam in mātrimōnium dat. perfacile factū esse illīs probat cōnāta perficere proptereā quod ipse suae cīvitātis imperium obtentūrus esset nōn esse dubium quīn tōtīus Galliae plūrimum Helvētiī possent sē suīs cōpiīs suōque exercitū illīs rēgna conciliātūrum cōnfirmat. hāc ōrātiōne adductī inter sē fidem et jūs jūrandum dant et rēgnō occupātō per trēs potentissimōs ac firmissimōs populōs tōtīus Galliae sēsē potīrī posse spērant. Ea rēs est Helvētiīs per indicium ēnūntiāta. mōribus suīs Orgetorigem ex vinculīs causam dīcere coēgērunt damnātum poenam sequī oportēbat ut ignī cremārētur. diē cōnstitūtā causae dictiōnis Orgetorix ad jūdicium omnem suam familiam ad hominum mīlia decem undique coēgit et omnēs clientēs obaerātōsque suōs quōrum magnum numerum habēbat eōdem condūxit per eōs nē causam dīceret sē ēripuit. cum cīvitās ob eam rem incitātā armīs jūs suum exsequī cōnārētur multitūdinemque hominum ex agrīs magistrātūs cōgerent Orgetorix mortuus est neque abest suspīciō ut Helvētiī arbitrantur quīn ipse sibi mortem cōnscīverit. Post ējus mortem nihilōminus Helvētiī id quod cōnstituerant facere cōnantur ut ē fīnibus suīs exeant. ubi  jam sē ad eam rem parātōs esse arbitrātī sunt oppida sua omnia numerō ad duodecim vīcōs ad quadringentōs reliqua prīvāta aedificia incendunt frūmentum omne praeter quod sēcum portātūrī erant combūrunt ut domum reditiōnis spē sublāta parātiōrēs ad omnia perīcula subeunda essent trium mēnsum molita cibāria sibi quemque domō efferre jubent. persuādent Rauracīs et Tulingīs et Latobrigīs fīnitimīs utī eōdem ūsī cōnsiliō oppidīs suīs vīcīsque exustīs ūna cum iīs proficīscantur Boiōsque quī trāns Rhēnum incoluerant et in agrum Nōricum trānsierant Norēiamque oppugnābant receptōs ad sē sociōs sibi adscīscunt.'
    test_class = Preprocessor(test_text, ['.', ';'], 'test')
    print(test_class.tokenize())
