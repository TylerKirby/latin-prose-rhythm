from prose_rhythm.preprocessor import Preprocessor
from prose_rhythm.analyze import Analyze
import os
import re
import codecs
import pandas as pd

cicero_texts_path = '/Users/tyler/Datasets/phi-macronized/cicero/'
analyze = Analyze()
text_paths = [cicero_texts_path+p for p in os.listdir(cicero_texts_path)]

df = pd.DataFrame()

for path in text_paths:
    with codecs.open(path, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    title = ' '.join([w.title() for w in path.split('/')[-1][:-4].split('_')])
    tokens = Preprocessor(text=text).tokenize()
    rhythms = analyze.get_rhythms(tokens, include_sentence=False)
    text_dict = analyze.rhythm_frequency(rhythms)
    text_dict['title'] = title
    text_dict['author'] = 'Cicero'
    text_df = pd.DataFrame(text_dict, index=[0])
    df = df.append(text_df, sort=True)

df.to_csv('cicero_rhythms.csv')