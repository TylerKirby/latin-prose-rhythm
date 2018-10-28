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

df.to_csv('../data/cicero_df_zielinski.csv', index=None)