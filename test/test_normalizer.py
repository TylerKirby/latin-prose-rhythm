"""
Unit tests for normalizer class.
"""

from prose_rhythm.normalizer import Normalizer


def test_replace_abbreviations():
    text_with_abbrev = "Puella Agr. puer M' putat Oct. vivat."
    text_without_abbrev = "Puella abbrev puer abbrev putat abbrev vivat."
    assert Normalizer(text_with_abbrev)._replace_abbreviations() == text_without_abbrev


def test_replace_roman_numerals():
    text_with_numerals = "XII Puer CCC vivat."
    text_without_numerals = "roman_numeral Puer roman_numeral vivat."
    assert Normalizer(text_with_numerals)._replace_roman_numerals() == text_without_numerals


def test_remove_extra_white_space():
    test_with_extra_white_space = " Puer putat vivat  puella   puer."
    test_without_extra_white_space = "Puer putat vivat puella puer."
    assert Normalizer(test_with_extra_white_space)._remove_extra_white_space() == \
           test_without_extra_white_space


def test_normalizer():
    text = "III. O tempora o morae!   Galliā, est Besta Agr. rogat?"
    normalized_text = "roman_numeral. o tempora o morae. galliā, est besta abbrev rogat."
    assert Normalizer(text).normalize() == normalized_text