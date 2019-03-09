import os

PATH = '/texts_for_analysis/'

paths = [PATH+file for file in os.listdir(PATH) if file != '.DS_Store']
texts = ['/'.join([dir, p]) for dir in paths for p in os.listdir(dir) if p != '.DS_Store']

script = []
for index, path in enumerate(texts):
    macronize_script = f'python macronize.py -i {path} -o {path} -v -j --maius\necho \"macronized text {index}\"\n'
    script.append(macronize_script)

with open('macronize_texts.sh', 'w') as f:
    for s in script:
        f.write(s)

