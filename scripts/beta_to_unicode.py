import os

from cltk.corpus.greek.tlgu import TLGU

tlgu = TLGU()

SOURCE_DIR = '/Users/tyler/Datasets/PHI/'
TARGET_DIR = '/Users/tyler/Datasets/phi-unicode/'

beta_txt_paths = [SOURCE_DIR+file for file in os.listdir(SOURCE_DIR) if file.endswith('.txt')]

for path in beta_txt_paths:
	filename = path.split('/')[-1]
	output_path = TARGET_DIR+filename
	tlgu.convert(input_path=path, output_path=output_path, latin=True, divide_works=True)
