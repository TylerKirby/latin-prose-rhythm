# Auceps syllabarum: a digital analysis of Latin prose rhythm
Code accompanying the paper *Auceps syllabarum: a digital analysis of Latin prose rhythm* by Tom Keeline and Tyler Kirby.

## Summary
There are three primary modules: `normalizer.py`, `preprocessor.py`, and `analyze.py`. The normalizer standardizes text for preprocessing. Note that it expects a macronized version of the PHI Latin texts. The preprocessor generates a Python dictionary of the text with all the necessary prosimetric data for each syllable. The analysis module processes the resulting tokens into various reports.

The original data for the tables found in the paper can be found under `data`.

To generate data tables based on the clausular topology delineated in the paper, run the `create_datasets.py` script with the appropriate path argument.

## Setup
Refer to the `jrs_sample` Jupyter notebook for an example workflow.
