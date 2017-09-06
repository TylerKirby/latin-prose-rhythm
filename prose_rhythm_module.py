"""
Module for analyzing the prose rhythm of Latin texts.
"""

from cltk.stem.latin.syllabifier import Syllabifier

# TODO: Define langauge variables
# TODO: Check for elision
# TODO: Check if syllabifier works

class prose_rhythm_module(object):
    def __init__(self, elision, sests, punctuation, text):
        self.elision = elision
        self.sests = sests
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
            syllabified.append(syllabified_words)
        return syllabified

if __name__ == "__main__":
    test_text = "Quo tandem usque, O Catilina; abutere nostra patientia."
    test = prose_rhythm_module(elision=True, sests=True, punctuation=[',', ';', '.'], text=test_text)
    preprocessed = test.preprocessed()
    print(preprocessed)
