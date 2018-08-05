# -*- coding: utf-8 -*-
"""
Unit tests for normalizer class.
"""

from prose_rhythm.normalizer import Normalizer

normalizer = Normalizer()


def test_replace_abbreviations():
    text_with_abbrev = "Puella Agr. puer M' putat Oct. vivat."
    text_without_abbrev = "Puella 00000 puer 00000 putat 00000 vivat."
    assert normalizer._replace_abbreviations(text_with_abbrev) == text_without_abbrev


def test_replace_roman_numerals():
    text_with_numerals = "XII Puer CCC vivat."
    text_without_numerals = "roman_numeral Puer roman_numeral vivat."
    assert normalizer._replace_roman_numerals(text_with_numerals) == text_without_numerals


def test_numerals_in_words():
    text = "Cui dono. Puer vīs."
    target = "Cui dono. Puer vīs."
    assert normalizer._replace_roman_numerals(text) == target


def test_vim_not_numeral():
    text = "Non vim puer."
    assert Normalizer()._replace_roman_numerals(text) == text
    text_start_with_vim = "Vim puer non."
    assert normalizer._replace_roman_numerals(text_start_with_vim) == text_start_with_vim


def test_dici_not_numeral():
    text = "Non dīcī puer."
    assert normalizer._replace_roman_numerals(text) == text


def test_remove_extra_white_space():
    test_with_extra_white_space = " Puer putat vivat  puella   puer."
    test_without_extra_white_space = "Puer putat vivat puella puer."
    assert normalizer._remove_extra_white_space(test_with_extra_white_space) == \
        test_without_extra_white_space


def test_remove_word_enjambments():
    text = "prī-\nnum"
    target = "prīnum"
    assert normalizer._remove_word_enjambments(text) == target
    text = "Puella eun- dem puer."
    target = "Puella eundem puer."
    assert normalizer._remove_word_enjambments(text) == target


def test_normalizer():
    text = "III. O tempora o morae!   Gal-\nliā, est Besta Agr. rogat?"
    normalized_text = "roman_numeral o tempora o morae. galliā, est besta 00000 rogat."
    assert normalizer.normalize(text) == normalized_text


def test_hicc_hocc():
    text = "Puer hic amat hoc puellam."
    target = "puer hicc amat hocc puellam."
    assert normalizer.normalize(text) == target


def test_remove_quotes():
    text = """Puella dicit: 'Quo puer est?'"""
    target = "puella dicit. quo puer est."
    assert normalizer.normalize(text) == target


def test_underscore_punc():
    text = """Quo puer?_, est puella."""
    target = "quo puer. est puella."
    assert normalizer.normalize(text) == target


def test_unde():
    text = "Vnde?"
    target = "unde."
    assert normalizer.normalize(text) == target
