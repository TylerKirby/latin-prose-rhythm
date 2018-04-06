# -*- coding: utf-8 -*-

from prose_rhythm.preprocessor import Preprocessor
from prose_rhythm.analyze import Analyze
from prose_rhythm.normalizer import Normalizer

path = "/Users/tyler/Projects/macronized_texts/Caesar_CivilWar_1-22-18.txt"

with open(path, 'r', encoding='utf8') as file:
    text = file.read()

tokens = Preprocessor(text=text).tokenize()

rhythm_list = Analyze().get_rhythms(tokens)
print(Analyze().rhythm_dict(rhythm_list))

