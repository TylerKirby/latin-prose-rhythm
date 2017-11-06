"""
Module for analyzing the prose rhythm of Latin texts.
"""

from cltk.stem.latin.syllabifier import Syllabifier
from cltk.stem.latin.j_v import JVReplacer

# TODO: Check for elision
# TODO: Rewrite preprocessing to remove numbers and punc not in self.punc


class prose_rhythm(object):

    SESTS = ['sc', 'sm', 'sp', 'st', 'z']
    MUTES = ['b', 'c', 'k', 'd', 'g', 'p', 't']
    DIGRAPHS = ['ch', 'ph', 'th', 'qu']
    LIQUIDS = ['r', 'l']
    VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']
    SINGLE_CONSONANTS = ['b', 'c', 'd', 'g', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'f', 'j']
    DOUBLE_CONSONANTS = ['x', 'z']
    LONG_VOWELS = ['ā', 'ē', 'ī', 'ō', 'ū']
    DIPHTHONGS = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']
    NASALS = ['m', 'n']

    def __init__(self, elision, sests, mute_plus_liquid, punctuation, text):
        self.elision = elision
        self.sests = sests
        self.mute_plus_liquid  = mute_plus_liquid
        self.punctuation = punctuation
        self.text = text

    def preprocessed_text(self):
        """
        Tokenize text on supplied characters.
        :return: tokenized text
        :rtype : list
        """
        default_seperator = self.punctuation[0]
        for punc in self.punctuation[1:]:
            self.text = self.text.replace(punc, default_seperator)
        return [sentence.strip() for sentence in self.text.split(default_seperator) if sentence.strip() is not '']

    def syllabified(self):
        """
        Syllabify text.
        :return: syllabified text
        :rtype : list
        """
        preprocessed_text = self.preprocessed_text()
        syllabifier = Syllabifier()
        syllabified_sentence = []
        for sentence in preprocessed_text:
            syllabified_words = [syllabifier.syllabify(word) for word in sentence.lower().split(' ') if '[' not in word]
            syllabified_sentence.append(syllabified_words)
        syllabified = [sentence for sentence in syllabified_sentence if [] not in sentence]
        return syllabified

    def long_by_nature(self, syllable):
        """
        Check if syllable is long by nature.
        :return: true if long by nature
        :rtype : boolean
        """
        for vowel in self.LONG_VOWELS:
            if vowel in syllable:
                return True
        for diphthong in self.DIPHTHONGS:
            if diphthong in syllable:
                return True
        return False

if __name__ == "__main__":
    test_text = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec uero necesse est quemquam a me nominari; vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me alienationem commendationem tibi ad impios civis fore putavisti iam iacio iacet."
    test = prose_rhythm(elision=True, sests=True, mute_plus_liquid=True, punctuation=[':',';','.','?','!'], text=test_text)
    preprocessed = test.syllabified()
    # print(preprocessed)
    print(JVReplacer().replace(test_text))
