import os
import re

PATH = '/Users/tyler/Desktop/texts_for_analysis/'
dirs = [PATH+p for p in os.listdir(PATH) if p != '.DS_Store']


def remove_extra_white_space(text):
    text = text.replace('\n', ' ')
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"^\s", "", text)
    return text

def remove_word_enjambments(text):
    text = remove_extra_white_space(text)
    tokens = [word.replace('- ', '').replace('-\n', '') for word in text.split(' ')]
    return ' '.join(tokens).replace('- ', '')

for dir in dirs:
    texts = ['/'.join([dir, p]) for p in os.listdir(dir) if p != '.DS_Store']
    for text in texts:
        with open(text, 'r', encoding='utf-8', errors='ignore') as f:
            text_contents = f.read()
        text_contents = text_contents.replace('ā', 'a')\
                                     .replace('ē', 'e')\
                                     .replace('ī', 'i')\
                                     .replace('ō', 'o')\
                                     .replace('ū', 'u')
        text_contents = remove_word_enjambments(text_contents)
        with open(text, 'w') as f:
            f.write(text_contents)