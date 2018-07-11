# -*- coding: utf-8 -*-
"""
Unit tests for methods in Preprocessor class.
"""

from prose_rhythm.preprocessor import Preprocessor


preprocessor3 = Preprocessor("test.")


def test_tokenize_syllables():
    test1 = preprocessor3._tokenize_syllables("mihi")
    test2 = preprocessor3._tokenize_syllables("ivi")
    test3 = preprocessor3._tokenize_syllables("audītū")
    test4 = preprocessor3._tokenize_syllables("conjiciō")
    test5 = preprocessor3._tokenize_syllables("ā")

    # syllable and index
    assert test1[0]["syllable"] == "mi"
    assert test1[0]["index"] == 0
    assert test1[1]["syllable"] == "hi"
    assert test1[1]["index"] == 1
    assert len(test1) == 2
    assert test2[0]["syllable"] == "i"
    assert test2[0]["index"] == 0
    assert test2[1]["syllable"] == "vi"
    assert test2[1]["index"] == 1
    assert len(test2) == 2
    assert test3[0]["syllable"] == "au"
    assert test3[0]["index"] == 0
    assert test3[1]["syllable"] == "dī"
    assert test3[1]["index"] == 1
    assert test3[2]["syllable"] == "tū"
    assert test3[2]["index"] == 2
    assert len(test3) == 3
    assert test4[0]["syllable"] == "con"
    assert test4[0]["index"] == 0
    assert test4[1]["syllable"] == "ji"
    assert test4[1]["index"] == 1
    assert test4[2]["syllable"] == "ci"
    assert test4[2]["index"] == 2
    assert test4[3]["syllable"] == "ō"
    assert test4[3]["index"] == 3
    assert len(test4) == 4
    assert test5[0]["syllable"] == "ā"
    assert test5[0]["index"] == 0
    assert len(test5) == 1

    # -gu digraph
    test8 = preprocessor3._tokenize_syllables("lingua")
    assert test8[0]["syllable"] == "lin"
    assert test8[1]["syllable"] == "gua"


def test_tokenize_syllables_long_by_nature():
    test1 = preprocessor3._tokenize_syllables("mihi")
    test2 = preprocessor3._tokenize_syllables("ivi")
    test3 = preprocessor3._tokenize_syllables("audītū")
    test4 = preprocessor3._tokenize_syllables("conjiciō")
    test5 = preprocessor3._tokenize_syllables("ā")

    assert test1[0]["long_by_nature"] == False
    assert test1[1]["long_by_nature"] == False
    assert test2[0]["long_by_nature"] == False
    assert test2[1]["long_by_nature"] == False
    assert test3[0]["long_by_nature"] == True
    assert test3[1]["long_by_nature"] == True
    assert test3[2]["long_by_nature"] == True
    assert test4[0]["long_by_nature"] == False
    assert test4[1]["long_by_nature"] == False
    assert test4[2]["long_by_nature"] == False
    assert test4[3]["long_by_nature"] == True
    assert test5[0]["long_by_nature"] == True


def test_tokenize_syllables_accent():
    test1 = preprocessor3._tokenize_syllables("mihi")
    test2 = preprocessor3._tokenize_syllables("ivi")
    test3 = preprocessor3._tokenize_syllables("audītū")
    test4 = preprocessor3._tokenize_syllables("conjiciō")
    test5 = preprocessor3._tokenize_syllables("ā")
    test6 = preprocessor3._tokenize_syllables("appelantur")

    # accent
    assert test1[0]["accented"] == True
    assert test1[1]["accented"] == False
    assert test2[0]["accented"] == True
    assert test2[1]["accented"] == False
    assert test3[0]["accented"] == False
    assert test3[1]["accented"] == True
    assert test3[2]["accented"] == False
    assert test4[0]["accented"] == False
    assert test4[1]["accented"] == True
    assert test4[2]["accented"] == False
    assert test4[3]["accented"] == False
    assert test5[0]["accented"] == True
    assert test6[0]["accented"] == False
    assert test6[1]["accented"] == False
    assert test6[2]["accented"] == True
    assert test6[3]["accented"] == False


def test_tokenize_syllables_long_by_position():
    test1 = preprocessor3._tokenize_syllables("mihi")
    test2 = preprocessor3._tokenize_syllables("ivi")
    test3 = preprocessor3._tokenize_syllables("audītū")
    test4 = preprocessor3._tokenize_syllables("conjiciō")
    test5 = preprocessor3._tokenize_syllables("ā")

    # long by position
    assert test1[0]["long_by_position"] == (False, None)
    assert test1[1]["long_by_position"] == (False, None)
    assert test2[0]["long_by_position"] == (False, None)
    assert test2[1]["long_by_position"] == (False, None)
    assert test3[0]["long_by_position"] == (False, None)
    assert test3[1]["long_by_position"] == (False, None)
    assert test3[2]["long_by_position"] == (False, None)
    assert test4[0]["long_by_position"] == (True, None)
    assert test4[1]["long_by_position"] == (False, None)
    assert test4[2]["long_by_position"] == (False, None)
    assert test4[3]["long_by_position"] == (False, None)
    assert test5[0]["long_by_position"] == (False, None)


def test_tokenize_syllables_mute_plus_liquid():
    # mute plus liquid
    test6 = preprocessor3._tokenize_syllables("volūcris")
    assert test6[1]["long_by_position"] == (False, "mute+liquid")
    test7 = preprocessor3._tokenize_syllables("oblinō")
    assert test7[0]["long_by_position"] == (True, None)
    gl_not_mute_liquid = preprocessor3._tokenize_syllables("neglēxit")
    assert gl_not_mute_liquid[1]["long_by_position"] == (True, None)


def test_tokenize_words():
    test1 = preprocessor3._tokenize_words("mihi conjiciō ivi it quam optāram auditū dedērunt te miror antōnī quorum.")

    # word and index
    assert test1[0]["word"] == "mihi"
    assert test1[0]["index"] == 0
    assert test1[1]["word"] == "conjiciō"
    assert test1[1]["index"] == 1
    assert len(test1) == 12
    # syllables and syllable count
    assert test1[0]["syllables"] == preprocessor3._tokenize_syllables("mihi")
    assert test1[1]["syllables_count"] == 4
    assert test1[3]["syllables_count"] == 1
def test_tokenize_words_elision():
    test1 = preprocessor3._tokenize_words("mihi conjiciō ivi it quam optāram auditū dedērunt te miror antōnī quorum.")
    test2 = preprocessor3._tokenize_words("Galliaque humanitate.")

    # elision
    assert test1[0]["syllables"][-1]["elide"] == (False, None)
    assert test1[3]["syllables"][-1]["elide"] == (False, None)
    assert test1[1]["syllables"][-1]["elide"] == (True, "strong")
    assert test1[2]["syllables"][-1]["elide"] == (True, "weak")
    assert test1[4]["syllables"][-1]["elide"] == (True, "strong")
    assert test2[0]["syllables"][-1]["elide"] == (True, "weak")
    test3 = preprocessor3._tokenize_words("Gallae est.")
    assert test3[0]["syllables"][-1]["elide"] == (True, "strong")
    test4 = preprocessor3._tokenize_words("Galliae haerum")
    assert test4[0]["syllables"][-1]["elide"] == (True, "strong")


def test_tokenize_words_long_by_position():
    # long by position inter word
    test = preprocessor3._tokenize_words("puella est bona it con.")
    assert test[3]["syllables"][-1]["long_by_position"] == (True, None)
    test2 = preprocessor3._tokenize_words("Commeant ad.")
    assert test2[0]["syllables"][-1]["long_by_position"] == (True, None)


def test_tokenize_words_sests():
    test3 = preprocessor3._tokenize_words("a spes co i no xe cta.")

    # sests test
    assert test3[0]["syllables"][0]["long_by_position"] == (False, "sest")
    assert test3[1]["syllables"][0]["long_by_position"] == (True, None)
    assert test3[2]["syllables"][0]["long_by_position"] == (False, None)
    assert test3[3]["syllables"][0]["long_by_position"] == (False, None)
    assert test3[4]["syllables"][0]["long_by_position"] == (True, None)
    assert test3[5]["syllables"][0]["long_by_position"] == (True, None)
