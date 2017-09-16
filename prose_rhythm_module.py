"""
Module for analyzing the prose rhythm of Latin texts.
"""

from cltk.stem.latin.syllabifier import Syllabifier

# TODO: Define langauge variables
# TODO: Check for elision
# TODO: Check if syllabifier works
# TODO: Combine 'qu' syllables for first sentence in sentence

class prose_rhythm_module(object):

    SEST = ['sc', 'sm', 'sp', 'st', 'z']
    MUTES = ['b', 'd', 'g', 'p', 't', 'c', 'k', 'ph', 'th', 'ch']
    LIQUIDS = ['r', 'l']

    def __init__(self, elision, sests, mute_plus_liquid, punctuation, text):
        self.elision = elision
        self.sests = sests
        self.mute_plus_liquid  = mute_plus_liquid
        self.punctuation = punctuation
        self.text = text

    @staticmethod
    def split(txt, seps):
        default_sep = seps[0]

        # we skip seps[0] because that's the default seperator
        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep)]

    def preprocessed(self):
        tokenized_cola = self.split(self.text, self.punctuation)
        syllabifier = Syllabifier()
        syllabified_sentence = []
        for sentence in tokenized_cola:
            syllabified_words = [syllabifier.syllabify(word) for word in sentence.lower().split(' ')]
            syllabified_sentence.append(syllabified_words)
        syllabified = [sentence for sentence in syllabified_sentence if [] not in sentence]
        return syllabified

if __name__ == "__main__":
    test_text = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec vero necesse est quemquam a me nominari; vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me alienationem commendationem tibi ad impios civis fore putavisti."
    test = prose_rhythm_module(elision=True, sests=True, mute_plus_liquid=True, punctuation=[',', ';', '.'], text=test_text)
    preprocessed = test.preprocessed()
    print(preprocessed)
