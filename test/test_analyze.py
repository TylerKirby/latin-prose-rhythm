"""
Unit tests for Analyze class
"""
from prose_rhythm.analyze import Analyze
from prose_rhythm.preprocessor import Preprocessor

analyze = Analyze()


def test_get_rhythms_elision():
    test = Preprocessor(text='sī quem habētis dēpōnite.').tokenize()
    correct = [('sī quem habētis dēpōnite', '-u----ux')]
    assert analyze.get_rhythms(test) == correct
    test = Preprocessor(text='esse ōrātiōnī locum.').tokenize()
    correct = [('esse ōrātiōnī locum', '---u--ux')]
    assert analyze.get_rhythms(test) == correct


def test_eu_not_diphthong():
    test = Preprocessor(text='locō superiōre impetum.').tokenize()
    correct = [('locō superiōre impetum', 'u-uuu--ux')]
    assert analyze.get_rhythms(test) == correct


def test_io_not_j():
    test = Preprocessor(text='sententiīs esse pereundum.').tokenize()
    correct = [('sententiīs esse pereundum', '--u--uuu-x')]
    assert analyze.get_rhythms(test) == correct