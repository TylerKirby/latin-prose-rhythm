import os

PHI_DIR = '/Users/tyler/Datasets/phi-unicode/'
OUTPUT_DIR = '/Users/tyler/Datasets/phi-macronized/'

paths = [(PHI_DIR+file, OUTPUT_DIR+file) for file in os.listdir(PHI_DIR) if file[:3] == 'lat']
print(paths[0])

for index, (input_path, output_path) in enumerate(paths):
    macronize_script = f'python macronize.py -i {input_path} -o {output_path} -v -j --maius\necho \"macronized text {index}\"\n'
    print(macronize_script)

