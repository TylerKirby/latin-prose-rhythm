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

preprocessor1 = Preprocessor(text=TEST_TEXT1, punctuation=[':', ';', '.', '?', '!'])
preprocessor2 = Preprocessor(text=TEST_TEXT2)

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




