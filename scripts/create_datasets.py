import os
import codecs
import argparse

from tqdm import tqdm
import pandas as pd

from prose_rhythm.preprocessor import Preprocessor
from prose_rhythm.analyze import Analyze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', '-a', required=True, type=str)
    args = parser.parse_args()


    text_path = '/Users/tyler/Datasets/phi-macronized/{}/'.format(args.author)
    analyze = Analyze()
    text_paths = [text_path + p for p in os.listdir(text_path) if p[0] != '.']

    rhythm_data = pd.DataFrame()

    for path in tqdm(text_paths):
        with codecs.open(path, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        title = ' '.join([w.title() for w in path.split('/')[-1][:-4].split('_')])
        tokens = Preprocessor(text=text).tokenize()
        rhythms = analyze.get_rhythms(tokens, include_sentence=False)
        text_dict = analyze.rhythm_frequency(rhythms)
        text_df = pd.DataFrame(text_dict, index=[0])
        total = len(rhythms)
        text_df['total'] = total - 5
        text_df['total_excluded'] = text_dict['total_excluded']
        text_df['abbrev_excluded'] = text_dict['abbrev_excluded']
        text_df['bracket_excluded'] = text_dict['bracket_excluded']
        text_df['short_excluded'] = text_dict['short_excluded']
        text_df['other_excluded'] = text_dict['other_excluded']
        rhythm_data = rhythm_data.append(text_df, sort=True)

    rhythm_data = rhythm_data.fillna(0)
    rhythm_data.to_csv('../data/{}_rhythms.csv'.format(args.author), index=None)
    rhythm_data = pd.read_csv('../data/{}_rhythms.csv'.format(args.author))

    texts = [text[:-4].replace('_', ' ') for text in os.listdir(text_path) if text[0] != '.']

    df = pd.DataFrame({ 'title': texts })
    df['total_clausulae'] = rhythm_data['total']
    df['total_excluded'] = rhythm_data['total_excluded']
    if df['total_excluded'] == -1: # texts with no breaks
        df['total_excluded'] = 0
    df['abbrev_excluded'] = rhythm_data['abbrev_excluded']
    df['bracket_excluded'] = rhythm_data['bracket_excluded']
    df['short_excluded'] = rhythm_data['short_excluded']

    def add_rhythm_col(col_name, rhythm):
        rhythm_df = rhythm_data[[col for col in rhythm_data.columns if rhythm in col]].copy()
        df['{} ({})'.format(col_name, rhythm)] = rhythm_df.sum(axis=1)

    def add_res_total_col(col_name, res_names):
        df[col_name] = df[[col for col in df.columns if res_names in col]].copy().sum(axis=1)

    def add_rhythm_total_col(col_name, col_names):
        df[col_name] = df[col_names].copy().sum(axis=1)

    def add_ex_rhythm_col(col_name, rhythm, ex_rhythms):
        rhythm_cols = [col for col in rhythm_data.columns if rhythm in col]
        ex_cols = []
        for e in ex_rhythms:
            ex_rhythm_cols = [col for col in rhythm_data.columns if e in col]
            ex_cols.append(ex_rhythm_cols)
        ex_rhythm_cols = [item for sublist in ex_cols for item in sublist]
        diff_cols = [r for r in rhythm_cols if r not in ex_rhythm_cols]
        rhythm_df = rhythm_data[diff_cols].copy()
        df['{} ({})'.format(col_name, rhythm)] = rhythm_df.sum(axis=1)

    # Cretic trochee
    add_rhythm_col('cretic-trochee', '-u--x')
    add_rhythm_col('cretic-trochee 1 res', 'uuu--x')
    add_rhythm_col('cretic-trochee 1 res', '-uuu-x')
    add_rhythm_col('cretic-trochee 1 res', '-u-uux')

    # double/molossus cretic
    add_rhythm_col('double/molossus-cretic pure double-cretic', '-u--ux')
    add_rhythm_col('double/molossus-cretic pure molossus-cretic', '----ux')
    add_rhythm_col('double/molossus-cretic 1 res', 'uuu--ux')
    add_rhythm_col('double/molossus-cretic 1 res', '-uuu-ux')
    add_rhythm_col('double/molossus-cretic 1 res', '-u-uuux')

    add_rhythm_col('double/molossus-cretic molossus not chor 1 res', 'uu---ux')
    add_rhythm_col('double/molossus-cretic molossus not chor 1 res', '--uu-ux')
    add_rhythm_col('double/molossus-cretic molossus not chor 1 res', '---uuux')

    add_rhythm_col('double/molossus-cretic chor res', '-uu--ux')

    add_rhythm_col('double/molossus-cretic ep res', '-u---ux')

    # Double trochee
    add_rhythm_col('double trochee', '-u-x')
    add_ex_rhythm_col('double trochee 1 res', 'uuu-x', ['-uuu-x'])
    add_ex_rhythm_col('double trochee 1 res', '-uuux', ['---uuux', '-u-uuux'])

    # Hypodochmiac
    add_rhythm_col('hypodochmiac', '-u-ux')
    add_ex_rhythm_col('hypodochmiac 1 res', 'uuu-ux', ['-uuu-ux'])
    # add_rhythm_col('hypodochmiac 1 res', 'uuu-ux')
    add_rhythm_col('hypodochmiac 1 res', '-uuuux')

    # Spondaic and dactylic
    add_rhythm_col('spondaic', '---x')
    add_rhythm_col('heroic', '-uu-x')

    # First paeon
    add_ex_rhythm_col('first paeon', '-uux', ['-u-uux'])

    # Choriamb trochee
    add_rhythm_col('choriamb trochee', '-uu--x')

    # Short sequence
    add_rhythm_col('short sequence', 'uuuuux')

    df['total_artistic'] = df.drop(columns=['total_clausulae', 'total_excluded', 'abbrev_excluded', 'bracket_excluded', 'short_excluded']).sum(axis=1)
    df['misc_clausulae'] = (df['total_clausulae'] - df['total_excluded']) - df['total_artistic']
    df['percent_clausulae'] = (df['total_artistic'] + df['misc_clausulae']) / (df['total_clausulae'] - df['total_excluded'])

    df.to_csv('../data/{}_df.csv'.format(args.author), index=None)
