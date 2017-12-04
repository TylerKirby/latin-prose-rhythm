"""
Unit tests for methods in Preprocessor class.
"""

from prose_rhythm_module.preprocessor import Preprocessor

TEST_TEXT1 = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit " \
            "hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec vero necesse est quemquam a me nominari; " \
            "vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum " \
            "facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum " \
            "inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut " \
            "audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me " \
            "alienationem commendationem tibi ad impios civis fore putavisti."
TEST_TEXT2 = "Mihi conicio iui it, quam optaram, auditu dederunt: te miror, Antoni, quorum. Iuuenum iuuo coniectus et si cetera; coniugo auctor uia uector."
TEST_TEXT3 = "Mihi coniciō iui it, quam optāram, auditū dedērunt: te miror, Antōnī, quorum. Iuuēnum iuuō coniectus et si cetera; coniugo auctor uiā uector."

preprocessor1 = Preprocessor(text=TEST_TEXT1, punctuation=[':', ';', '.', '?', '!'])
preprocessor2 = Preprocessor(text=TEST_TEXT2)
preprocessor3 = Preprocessor(text=TEST_TEXT3)

def test_u_to_v():
    # word begins with 'u'
    assert preprocessor1._u_to_v("uita") == "vita"
    assert preprocessor1._u_to_v("ultor") == "ultor"
    assert preprocessor1._u_to_v("uae") == "vae"
    # word ends with 'u'
    assert preprocessor1._u_to_v("auditu") == "auditu"
    assert preprocessor1._u_to_v("arcu") == "arcu"
    # vowel + u + vowel
    assert preprocessor1._u_to_v("amaui") == "amavi"
    # consonant + u + consonant
    assert preprocessor1._u_to_v("amatus") == "amatus"
    # uu case 1
    assert preprocessor1._u_to_v("uua") == "uva"
    # uu case 2
    assert preprocessor1._u_to_v("uulnus") == "vulnus"
    # uu case 3
    assert preprocessor1._u_to_v("uult") == "vult"
    # vowel + u + consontant
    assert preprocessor1._u_to_v("auctor") == "auctor"
    # consonant + u + vowel
    assert preprocessor1._u_to_v("habui") == "habui"
    assert preprocessor1._u_to_v("habuerit") == "habuerit"
    assert preprocessor1._u_to_v("imbuantur") == "imbuantur"
    # consonant + u + u + consonant
    assert preprocessor1._u_to_v("tuus") == "tuus"
    assert preprocessor1._u_to_v("mortuus") == "mortuus"
    assert preprocessor1._u_to_v("perpetuum") == "perpetuum"
    assert preprocessor1._u_to_v("fluuius") == "fluvius"
    assert preprocessor1._u_to_v("exuuiae") == "exuviae"
    # consonant + u + vowel (not i)
    assert preprocessor1._u_to_v("alueo") == "alveo"
    # consonant + u + vowel (i)
    assert preprocessor1._u_to_v("inuitat") == "invitat"
    # consonantal i at start of word
    assert preprocessor1._u_to_v("iuuenum") == "iuvenum"
    # extras
    assert preprocessor1._u_to_v("adiuuo") == "adiuvo"
    assert preprocessor1._u_to_v("iui") == "ivi"

def test_i_to_j():
    # initial i + consonant (not u/v)
    assert preprocessor1._i_to_j("incoctus") == "incoctus"
    assert preprocessor1._i_to_j("ignis") == "ignis"
    assert preprocessor1._i_to_j("it") == "it"
    # initial i + vowel (not u/v)
    assert preprocessor1._i_to_j("iaceo") == "jaceo"
    assert preprocessor1._i_to_j("iecur") == "jecur"
    assert preprocessor1._i_to_j("iocus") == "jocus"
    # initial i + u/v
    assert preprocessor1._i_to_j("iubeo") == "jubeo"
    assert preprocessor1._i_to_j("ius") == "jus"
    assert preprocessor1._i_to_j("ivi") == "ivi"
    # i after prefix
    assert preprocessor1._i_to_j("adicio") == "adjicio"
    assert preprocessor1._i_to_j("adiectus") == "adjectus"
    assert preprocessor1._i_to_j("abicio") == "abjicio"
    assert preprocessor1._i_to_j("abiectus") == "abjectus"
    assert preprocessor1._i_to_j("conicio") == "conjicio"
    assert preprocessor1._i_to_j("coniectus") == "conjectus"
    assert preprocessor1._i_to_j("subicio") == "subjicio"
    assert preprocessor1._i_to_j("subiectus") == "subjectus"
    assert preprocessor1._i_to_j("adiudico") == "adjudico"
    assert preprocessor1._i_to_j("coniuro") == "conjuro"
    assert preprocessor1._i_to_j("coniungo") == "conjungo"
    assert preprocessor1._i_to_j("coniunctus") == "conjunctus"
    assert preprocessor1._i_to_j("adiuvo") == "adjuvo"

def test_i_u_to_j_v():
   CORRECT1 = "mihi conjicio ivi it, quam optaram, auditu dederunt: te miror, antoni, quorum. juvenum juvo conjectus et si cetera; conjugo auctor via vector."
   assert preprocessor2._i_u_to_j_v() == CORRECT1

def test_tokenize_syllables():
    test1 = preprocessor3._tokenize_syllables("mihi")
    test2 = preprocessor3._tokenize_syllables("ivi")
    test3 = preprocessor3._tokenize_syllables("audītū")
    test4 = preprocessor3._tokenize_syllables("conjiciō")
    test5 = preprocessor3._tokenize_syllables("ā")
    # syllable and index
    assert test1[0]["syllable"] == "mi"
    assert test1[0]["index"] == 0
    assert test1[1]["syllable"] ==  "hi"
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
    # long by nature
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
    # long by position
    assert test1[0]["long_by_position"] == False
    assert test1[1]["long_by_position"] == False
    assert test2[0]["long_by_position"] == False
    assert test2[1]["long_by_position"] == False
    assert test3[0]["long_by_position"] == False
    assert test3[1]["long_by_position"] == False
    assert test3[2]["long_by_position"] == False
    assert test4[0]["long_by_position"] == True
    assert test4[1]["long_by_position"] == False
    assert test4[2]["long_by_position"] == False
    assert test4[3]["long_by_position"] == False
    assert test5[0]["long_by_position"] == False

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
    # elision
    assert "elide" not in test1[0]["syllables"][-1]
    assert "elide" not in test1[3]["syllables"][-1]
    assert test1[1]["syllables"][-1]["elide"] == (True, "strong")
    assert test1[2]["syllables"][-1]["elide"] == (True, "weak")
    assert test1[4]["syllables"][-1]["elide"] == (True, "strong")
    # long by position inter word
    test2 = preprocessor3._tokenize_words("puella est bona it con.")
    assert test2[3]["syllables"][-1]["long_by_position"] == True
    # sests test
    test3 = preprocessor3._tokenize_words("a spes co i no xe cta.")
    assert test3[0]["syllables"][0]["long_by_position"] == (False, "sest")
    assert test3[1]["syllables"][0]["long_by_position"] == True
    assert test3[2]["syllables"][0]["long_by_position"] == False
    assert test3[3]["syllables"][0]["long_by_position"] == False
    assert test3[4]["syllables"][0]["long_by_position"] == True
    assert test3[5]["syllables"][0]["long_by_position"] == True
