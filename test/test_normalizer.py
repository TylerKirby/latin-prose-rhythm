"""
Unit tests for normalizer class.
"""

from prose_rhythm.normalizer import Normalizer


def test_replace_abbreviations():
    text_with_abbrev = "Puella Agr. puer M' putat Oct. vivat."
    text_without_abbrev = "Puella abbrev puer abbrev putat abbrev vivat."
    assert Normalizer(text_with_abbrev)._replace_abbreviations() == text_without_abbrev


def test_remove_roman_numerals():
    text_with_numerals = "XII Puer putat vivat XXX puella III VL puer."
    text_without_numerals = " Puer putat vivat  puella   puer."
    assert Normalizer(text_with_numerals)._remove_roman_numerals() == text_without_numerals


def test_remove_extra_white_space():
    test_with_extra_white_space = " Puer putat vivat  puella   puer."
    test_without_extra_white_space = "Puer putat vivat puella puer."
    assert Normalizer(test_with_extra_white_space)._remove_extra_white_space() == \
           test_without_extra_white_space


def test_normalizer():
    text = "III. O tempora o morae!   Galliā, est Besta Agr. rogat?"
    normalized_text = ". o tempora o morae. galliā, est besta abbrev rogat."
    assert Normalizer(text).normalize() == normalized_text