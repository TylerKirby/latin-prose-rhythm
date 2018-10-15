"""
Script to transform raw Cicero data into Zielinski typology numbers.
Duplicate categories are currently commented out.
"""

import os
import collections
import pandas as pd

text_path = '/Users/tyler/Datasets/phi-macronized/cicero/'

texts = [text[:-4].replace('_', ' ') for text in os.listdir(text_path)]

rhythm_data = pd.read_csv('../data/cicero_rhythms.csv')

rhythm_types = []

df = pd.DataFrame({ 'title': texts })
df['total_clausulae'] = rhythm_data['total']
df['total_excluded'] = rhythm_data['total_excluded']
df['abbrev_excluded'] = rhythm_data['abbrev_excluded']
df['bracket_excluded'] = rhythm_data['bracket_excluded']
df['short_excluded'] = rhythm_data['short_excluded']

def add_rhythm_col(col_name, rhythm):
    rhythm_df = rhythm_data[[col for col in rhythm_data.columns if rhythm in col]].copy()
    df['{} ({})'.format(col_name, rhythm)] = rhythm_df.sum(axis=1)
    rhythm_types.append(rhythm)

def add_res_total_col(col_name, res_names):
    df[col_name] = df[[col for col in df.columns if res_names in col]].copy().sum(axis=1)

def add_rhythm_total_col(col_name, col_names):
    df[col_name] = df[col_names].copy().sum(axis=1)

def add_ex_rhythm_col(col_name, rhythm, ex_rhythm):
    rhythm_cols = [col for col in rhythm_data.columns if rhythm in col]
    ex_rhythm_cols = [col for col in rhythm_data.columns if ex_rhythm in col]
    diff_cols = [r for r in rhythm_cols if r not in ex_rhythm_cols]
    rhythm_df = rhythm_data[diff_cols].copy()
    df['{} ({})'.format(col_name, rhythm)] = rhythm_df.sum(axis=1)
    rhythm_types.append(rhythm)

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
add_ex_rhythm_col('double trochee 1 res', 'uuu-x', '-uuu-x')
add_ex_rhythm_col('double trochee 1 res', '-uuux', '---uuux')

# Hypodochmiac
add_rhythm_col('hypodochmiac', '-u-ux')
add_rhythm_col('hypodochmiac 1 res', 'uuuu-ux')
add_rhythm_col('hypodochmiac 1 res', '-uuuux')

# Spondaic and dactylic
add_rhythm_col('spondaic', '---x')
add_rhythm_col('heroic', '-uu-x')

df.to_csv('../data/cicero_df_zielinski.csv', index=None)

duplicates = [item for item, count in collections.Counter(rhythm_types).items() if count > 1]
if len(duplicates) > 0:
    print('You have duplicate rhythms!')
    print(duplicates)
else:
    print('No duplicates found.')
