import os
import pandas as pd

text_path = '/Users/tyler/Datasets/phi-macronized/cicero/'

texts = [text[:-4].replace('_', ' ') for text in os.listdir(text_path)]

rhythm_data = pd.read_csv('../data/cicero_rhythms.csv')

df = pd.DataFrame({ 'title': texts })
df['total clausulae'] = rhythm_data['total']

def add_rhythm_col(col_name, rhythm):
    rhythm_df = rhythm_data[[col for col in rhythm_data.columns if rhythm in col]].copy()
    df['{} ({})'.format(col_name, rhythm)] = rhythm_df.sum(axis=1)

def add_res_total_col(col_name, res_names):
    df[col_name] = df[[col for col in df.columns if res_names in col]].copy().sum(axis=1)

def add_rhythm_total_col(col_name, col_names):
    df[col_name] = df[col_names].copy().sum(axis=1)

# Cretic-trochee
add_rhythm_col('cretic-trochee', '-u--x')

add_rhythm_col('cretic-trochee 1 res', 'uuu--x')
add_rhythm_col('cretic-trochee 1 res', '-uuu-x')
add_rhythm_col('cretic-trochee 1 res', '-u-uux')
add_res_total_col('cretic-trochee 1 res total', 'cretic-trochee 1 res')
add_rhythm_col('cretic-trochee 2 res', 'uuuuu-x')
add_rhythm_col('cretic-trochee 2 res', 'uuu-uux')
add_rhythm_col('cretic-trochee 2 res', '-uuuuux')
add_res_total_col('cretic-trochee 2 res total', 'cretic-trochee 2 res')
add_rhythm_total_col('cretic-trochee pure+res total', ['cretic-trochee (-u--x)', 'cretic-trochee 1 res total', 'cretic-trochee 2 res total'])

add_rhythm_col('cretic-trochee chor res', '-uu--x')
add_rhythm_col('cretic-trochee chor 1 res', 'uuuu--x')
add_rhythm_col('cretic-trochee chor 1 res', '-uuuu-x')
add_rhythm_col('cretic-trochee chor 1 res', '-uu-uux')
add_res_total_col('cretic-trochee chor 1 res total', 'cretic-trochee chor 1 res')
add_rhythm_total_col('cretic-trochee chor total', ['cretic-trochee chor res (-uu--x)', 'cretic-trochee chor 1 res total'])

add_rhythm_col('cretic-trochee ep res', '-u---x')
add_rhythm_col('cretic-trochee ep 1 res', 'uuu---x')
add_rhythm_col('cretic-trochee ep 1 res', '-uuu--x')
add_rhythm_col('cretic-trochee ep 1 res', '-u-uu-x')
add_rhythm_col('cretic-trochee ep 1 res', '-u--uux')
add_res_total_col('cretic-trochee ep 1 res total', 'cretic-trochee ep 1 res')
add_rhythm_total_col('cretic-trochee ep total', ['cretic-trochee ep res (-u---x)', 'cretic-trochee ep 1 res total'])

add_rhythm_total_col('cretic-trochee total', ['cretic-trochee pure+res total', 'cretic-trochee chor total', 'cretic-trochee ep total'])

# double/molossus-cretic
add_rhythm_col('double/molossus-cretic pure double-cretic', '-u--ux')
add_rhythm_col('double/molossus-cretic pure molossus-cretic', '----ux')

add_rhythm_col('double/molossus-cretic 1 res', 'uuu--ux')
add_rhythm_col('double/molossus-cretic 1 res', '-uuu-ux')
add_rhythm_col('double/molossus-cretic 1 res', '-u-uuux')
add_res_total_col('double/molossus-cretic 1 res total', 'double/molossus-cretic 1 res')
add_rhythm_col('double/molossus-cretic 2 res', 'uuuuu-ux')
add_rhythm_col('double/molossus-cretic 2 res', 'uuu-uuux')
add_rhythm_col('double/molossus-cretic 2 res', '-uuuuuux')
add_res_total_col('double/molossus-cretic 2 res total', 'double/molossus-cretic 2 res')
add_rhythm_total_col('double/molossus-cretic pure+res total', [
    'double/molossus-cretic pure double-cretic (-u--ux)',
    'double/molossus-cretic pure molossus-cretic (----ux)',
    'double/molossus-cretic 1 res total',
    'double/molossus-cretic 2 res total'
])

add_rhythm_col('double/molossus-cretic molossus not chor 1 res', 'uu---ux')
add_rhythm_col('double/molossus-cretic molossus not chor 1 res', '--uu-ux')
add_rhythm_col('double/molossus-cretic molossus not chor 1 res', '---uuux')
add_rhythm_col('double/molossus-cretic molossus not chor 2 res', 'uu-uu-ux')
add_rhythm_col('double/molossus-cretic molossus not chor 2 res', 'uu--uuux')
add_rhythm_col('double/molossus-cretic molossus not chor 2 res', '--uuuuux')
add_res_total_col('double/molossus-cretic molossus not chor 1 res total', 'double/molossus-cretic molossus not chor 1 res')
add_res_total_col('double/molossus-cretic molossus not chor 2 res total', 'double/molossus-cretic molossus not chor 2 res')
add_rhythm_total_col('double/molossus-cretic molossus not chor total', [
    'double/molossus-cretic molossus not chor 1 res total',
    'double/molossus-cretic molossus not chor 2 res total',
])

add_rhythm_col('double/molossus-cretic chor res', '-uu--ux')
add_rhythm_col('double/molossus-cretic chor 1 res', 'uuuu--ux')
add_rhythm_col('double/molossus-cretic chor 1 res', '-uuuu-ux')
add_rhythm_col('double/molossus-cretic chor 1 res', '-uu-uuux')
add_res_total_col('double/molossus-cretic chor 1 res total', 'double/molossus-cretic chor res (-uu--ux)')
add_rhythm_total_col('double/molossus-cretic chor total', [
    'double/molossus-cretic chor res (-uu--ux)',
    'double/molossus-cretic chor 1 res total'
])

add_rhythm_col('double/molossus-cretic ep res', '-u---ux')
add_rhythm_col('double/molossus-cretic ep 1 res', 'uuu---ux')
add_rhythm_col('double/molossus-cretic ep 1 res', '-uuu--ux')
add_rhythm_col('double/molossus-cretic ep 1 res', '-u-uu-ux')
add_rhythm_col('double/molossus-cretic ep 1 res', '-u--uuux')
add_res_total_col('double/molossus-cretic ep 1 res total', 'double/molossus-cretic ep 1 res')
add_rhythm_total_col('double/molossus-cretic ep total', [
    'double/molossus-cretic ep res (-u---ux)',
    'double/molossus-cretic ep 1 res total'
])

add_rhythm_total_col('double/molossus-cretic total', [
    'double/molossus-cretic pure+res total',
    'double/molossus-cretic chor total',
    'double/molossus-cretic ep total',
    'double/molossus-cretic molossus not chor total'
])

# cretic/molossus-double-trochee
add_rhythm_col('cretic/molossus-double-trochee pure cretic-double-trochee', '-u--u-x')
add_rhythm_col('cretic/molossus-double-trochee pure molossus-double-trochee', '----u-x')

add_rhythm_col('cretic/molossus-double-trochee 1 res', 'uuu--u-x')
add_rhythm_col('cretic/molossus-double-trochee 1 res', '-uuu-u-x')
add_rhythm_col('cretic/molossus-double-trochee 1 res', '-u-uuu-x')
add_rhythm_col('cretic/molossus-double-trochee 1 res', '-u--uuux')
add_res_total_col('cretic/molossus-double-trochee 1 res total', 'cretic/molossus-double-trochee 1 res')
add_rhythm_col('cretic/molossus-double-trochee 2 res', 'uuuuu-u-x')
add_rhythm_col('cretic/molossus-double-trochee 2 res', 'uuu-uuu-x')
add_rhythm_col('cretic/molossus-double-trochee 2 res', 'uuu--uuux')
add_rhythm_col('cretic/molossus-double-trochee 2 res', '-uuuuuu-x')
add_rhythm_col('cretic/molossus-double-trochee 2 res', '-uuu-uuux')
add_rhythm_col('cretic/molossus-double-trochee 2 res', '-u-uuuuux')
add_res_total_col('cretic/molossus-double-trochee 2 res total', 'cretic/molossus-double-trochee 2 res')
add_rhythm_total_col('cretic/molossus-double-trochee pure+res total', [
    'cretic/molossus-double-trochee pure cretic-double-trochee (-u--u-x)',
    'cretic/molossus-double-trochee pure molossus-double-trochee (----u-x)',
    'cretic/molossus-double-trochee 1 res total',
    'cretic/molossus-double-trochee 2 res total'
])

add_rhythm_col('cretic/molossus-double-trochee molossus not chor 1 res', 'uu---u-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 1 res', '--uu-u-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 1 res', '---uuu-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 1 res', '----uuux')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 2 res', 'uu-uu-u-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 2 res', 'uu--uuu-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 2 res', 'uu---uuux')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 2 res', '--uuuuu-x')
add_rhythm_col('cretic/molossus-double-trochee molossus not chor 2 res', '--uu-uuux')
add_res_total_col('cretic/molossus-double-trochee molossus not chor 1 res total', 'cretic/molossus-double-trochee molossus not chor 1 res')
add_res_total_col('cretic/molossus-double-trochee molossus not chor 2 res total', 'cretic/molossus-double-trochee molossus not chor 2 res')
add_rhythm_total_col('cretic/molossus-double-trochee molossus not chor total', [
    'cretic/molossus-double-trochee molossus not chor 1 res total',
    'cretic/molossus-double-trochee molossus not chor 2 res total',
])

add_rhythm_col('cretic/molossus-double-trochee chor res', '-uu--u-x')
add_rhythm_col('cretic/molossus-double-trochee chor 1 res', 'uuuu--u-x')
add_rhythm_col('cretic/molossus-double-trochee chor 1 res', '-uuuu-u-x')
add_rhythm_col('cretic/molossus-double-trochee chor 1 res', '-uu-uuu-x')
add_rhythm_col('cretic/molossus-double-trochee chor 1 res', '-uu--uuux')
add_res_total_col('cretic/molossus-double-trochee chor 1 res total', 'cretic/molossus-double-trochee chor 1 res')
add_rhythm_total_col('cretic/molossus-double-trochee chor total', [
    'cretic/molossus-double-trochee chor res (-uu--u-x)',
    'cretic/molossus-double-trochee chor 1 res total'
])

add_rhythm_col('cretic/molossus-double-trochee ep res', '-u---u-x')
add_rhythm_col('cretic/molossus-double-trochee ep 1 res', 'uuu---u-x')
add_rhythm_col('cretic/molossus-double-trochee ep 1 res', '-uuu--u-x')
add_rhythm_col('cretic/molossus-double-trochee ep 1 res', '-u-uu-u-x')
add_rhythm_col('cretic/molossus-double-trochee ep 1 res', '-u--uuu-x')
add_rhythm_col('cretic/molossus-double-trochee ep 1 res', '-u---uuux')
add_res_total_col('cretic/molossus-double-trochee ep 1 res total', 'cretic/molossus-double-trochee ep 1 res')
add_rhythm_total_col('cretic/molossus-double-trochee ep total', [
    'cretic/molossus-double-trochee ep res (-u---u-x)',
    'cretic/molossus-double-trochee ep 1 res total'
])

add_rhythm_total_col('cretic/molossus-double-trochee total', [
    'cretic/molossus-double-trochee pure+res total',
    'cretic/molossus-double-trochee chor total',
    'cretic/molossus-double-trochee ep total',
    'cretic/molossus-double-trochee molossus not chor total'
])

# cretic/molossus-hypodochmiac
add_rhythm_col('cretic/molossus-hypodochmiac pure cretic-hypodochmiac', '-u--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac pure molossus-hypodochmiac', '----u-ux')

add_rhythm_col('cretic/molossus-hypodochmiac 1 res', 'uuu--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 1 res', '-uuuu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 1 res', '-u-uuuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 1 res', '-u--uuuux')
add_res_total_col('cretic/molossus-hypodochmiac 1 res total', 'cretic/molossus-hypodochmiac 1 res')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', 'uuuuu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', 'uuu-uuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', 'uuu--uuuux')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', '-uuuuuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', '-uuu-uuuux')
add_rhythm_col('cretic/molossus-hypodochmiac 2 res', '-u-uuuuuux')
add_res_total_col('cretic/molossus-hypodochmiac 2 res total', 'cretic/molossus-hypodochmiac 2 res')
add_rhythm_total_col('cretic/molossus-hypodochmiac pure+res total', [
    'cretic/molossus-hypodochmiac pure cretic-hypodochmiac (-u--u-ux)',
    'cretic/molossus-hypodochmiac pure molossus-hypodochmiac (----u-ux)',
    'cretic/molossus-hypodochmiac 1 res total',
    'cretic/molossus-hypodochmiac 2 res total'
])

add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 1 res', '-uu--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 1 res', '--uu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 1 res', '---uuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 1 res', '----uuuux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', 'uu-uu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', 'uu--uuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', 'uu---uuuux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', '--uuuuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', '--uu-uuuux')
add_rhythm_col('cretic/molossus-hypodochmiac molossus not chor 2 res', '---uuuuuux')
add_res_total_col('cretic/molossus-hypodochmiac molossus not chor 1 res total', 'cretic/molossus-hypodochmiac molossus not chor 1 res')
add_res_total_col('cretic/molossus-hypodochmiac molossus not chor 2 res total', 'cretic/molossus-hypodochmiac molossus not chor 2 res')
add_rhythm_total_col('cretic/molossus-hypodochmiac molossus not chor total', [
    'cretic/molossus-hypodochmiac molossus not chor 1 res total',
    'cretic/molossus-hypodochmiac molossus not chor 2 res total',
])

add_rhythm_col('cretic/molossus-hypodochmiac chor res', '-uu--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac chor 1 res', 'uuuu--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac chor 1 res', '-uuuu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac chor 1 res', '-uu-uuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac chor 1 res', '-uu--uuuux')
add_res_total_col('cretic/molossus-hypodochmiac chor 1 res total', 'cretic/molossus-hypodochmiac chor 1 res')
add_rhythm_total_col('cretic/molossus-hypodochmiac chor total', [
    'cretic/molossus-hypodochmiac chor res (-uu--u-ux)',
    'cretic/molossus-hypodochmiac chor 1 res total'
])

add_rhythm_col('cretic/molossus-hypodochmiac ep res', '-u---u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac ep 1 res', 'uuu---u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac ep 1 res', '-uuu--u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac ep 1 res', '-u-uu-u-ux')
add_rhythm_col('cretic/molossus-hypodochmiac ep 1 res', '-u--uuu-ux')
add_rhythm_col('cretic/molossus-hypodochmiac ep 1 res', '-u---uuuux')
add_res_total_col('cretic/molossus-hypodochmiac ep 1 res total', 'cretic/molossus-hypodochmiac ep 1 res')
add_rhythm_total_col('cretic/molossus-hypodochmiac ep total', [
    'cretic/molossus-hypodochmiac ep res (-u---u-ux)',
    'cretic/molossus-hypodochmiac ep 1 res total'
])

add_rhythm_total_col('cretic/molossus-hypodochmiac total', [
    'cretic/molossus-hypodochmiac pure+res total',
    'cretic/molossus-hypodochmiac chor total',
    'cretic/molossus-hypodochmiac ep total',
    'cretic/molossus-hypodochmiac molossus not chor total'
])

# iambic and trochaic
add_rhythm_col('iambic/trochaic', '-u--u-u-x')
add_rhythm_col('iambic/trochaic', '-u--u-u-ux')
add_rhythm_col('iambic/trochaic', '-u--u-u-u-x')
add_rhythm_col('iambic/trochaic', '-u--u-u-u-ux')
add_res_total_col('iambic/trochaic total', 'iambic/trochaic')

# spondaic and dactylic
add_rhythm_col('spondaic/dactylic', '----x')
add_rhythm_col('spondaic/dactylic heroic', '-uu-x')
add_res_total_col('spondaic/dactylic total', 'spondaic/dactylic')

df.to_csv('../data/cicero_df.csv', index=None)