"""
Module for analyzing the prose rhythm of Latin texts.
"""

from cltk.stem.latin.syllabifier import Syllabifier

# TODO: Define langauge variables
# TODO: Check for elision
# TODO: Check if syllabifier works

class prose_rhythm_module(object):
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
        syllabified = []
        for sentence in tokenized_cola:
            syllabified_words = [syllabifier.syllabify(word) for word in sentence.split(' ')]
            syllabified.append(syllabified_words if syllabified_words not [])
        return syllabified

if __name__ == "__main__":
    test_text = "Quo tandem usque, O Catilina; abutere nostra patientia."
    test = prose_rhythm_module(elision=True, sests=True, mute_plus_liquid=True, punctuation=[',', ';', '.'], text=test_text)
    preprocessed = test.preprocessed()
    print(preprocessed)
