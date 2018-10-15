import os
import codecs
from tqdm import tqdm
import pandas as pd

from prose_rhythm.preprocessor import Preprocessor
from prose_rhythm.analyze import Analyze

cicero_texts_path = '/Users/tyler/Datasets/phi-macronized/cicero/'
analyze = Analyze()
text_paths = [cicero_texts_path+p for p in os.listdir(cicero_texts_path)]

df = pd.DataFrame()

for path in tqdm(text_paths):
    with codecs.open(path, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    title = ' '.join([w.title() for w in path.split('/')[-1][:-4].split('_')])
    tokens = Preprocessor(text=text).tokenize()
    rhythms = analyze.get_rhythms(tokens, include_sentence=False)
    text_dict = analyze.rhythm_frequency(rhythms)
    text_df = pd.DataFrame(text_dict, index=[0])
    total = len(rhythms)
    text_df['total'] = total - 3
    text_df['total_excluded'] = text_dict['total_excluded']
    text_df['abbrev_excluded'] = text_dict['abbrev_excluded']
    text_df['bracket_excluded'] = text_dict['bracket_excluded']
    text_df['short_excluded'] = text_dict['short_excluded']
    df = df.append(text_df, sort=True)

df = df.fillna(0)
df.to_csv('../data/cicero_rhythms.csv', index=None)
