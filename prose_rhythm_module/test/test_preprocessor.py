"""
Unit tests for methods in Preprocessor class.
"""

from prose_rhythm_module.preprocessor import Preprocessor

TEST_TEXT = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit " \
            "hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec vero necesse est quemquam a me nominari; " \
            "vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum " \
            "facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum " \
            "inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut " \
            "audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me " \
            "alienationem commendationem tibi ad impios civis fore putavisti."

preprocessor = Preprocessor(text=TEST_TEXT, punctuation=[':', ';', '.', '?', '!'])


def test_preprocessed_text():
	correct = ['[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit hostis, qui non bellum eodem tempore mihi quoque indixerit', 'Nec vero necesse est quemquam a me nominari', 'vobiscum ipsi recordamini', 'Mihi poenarum illi plus, quam optaram, dederunt', 'te miror, Antoni, quorum facta imitere, eorum exitus non perhorrescere', 'Atque hoc in aliis minus mirabar', 'Nemo enim illorum inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti', 'Tu ne verbo quidem violatus, ut audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me alienationem commendationem tibi ad impios civis fore putavisti']
	assert preprocessor.preprocessed_text() == correct

def test_syllabified():
	correct = [[['quo', 'nam'], ['me', 'o'], ['fa', 'to,'], ['pa', 'tres'], ['con', 'scrip', 'ti,'], ['fi', 'e', 'ri'], ['di', 'cam,'], ['ut'], ['ne', 'mo'], ['his'], ['an', 'nis'], ['vi', 'gin', 'ti'], ['rei'], ['pu', 'bli', 'cae'], ['fu', 'e', 'rit'], ['hos', 'tis,'], ['qui'], ['non'], ['bel', 'lum'], ['e', 'o', 'dem'], ['tem', 'po', 're'], ['mi', 'hi'], ['quo', 'que'], ['in', 'di', 'xe', 'rit']], [['nec'], ['ve', 'ro'], ['ne', 'ces', 'se'], ['est'], ['quem', 'quam'], ['a'], ['me'], ['no', 'mi', 'na', 'ri']], [['vo', 'bis', 'cum'], ['ip', 'si'], ['re', 'cor', 'da', 'mi', 'ni']], [['mi', 'hi'], ['poe', 'na', 'rum'], ['il', 'li'], ['plus,'], ['quam'], ['op', 'ta', 'ram,'], ['de', 'de', 'runt']], [['te'], ['mi', 'ror,'], ['an', 'to', 'ni,'], ['quo', 'rum'], ['fac', 'ta'], ['i', 'mi', 'te', 're,'], ['e', 'o', 'rum'], ['ex', 'i', 'tus'], ['non'], ['per', 'hor', 'res', 'ce', 're']], [['at', 'que'], ['hoc'], ['in'], ['a', 'li', 'is'], ['mi', 'nus'], ['mi', 'ra', 'bar']], [['ne', 'mo'], ['e', 'nim'], ['il', 'lo', 'rum'], ['in', 'i', 'mi', 'cus'], ['mi', 'hi'], ['fu', 'it'], ['vo', 'lun', 'ta', 'ri', 'us,'], ['om', 'nes'], ['a'], ['me'], ['rei'], ['pu', 'bli', 'cae'], ['cau', 'sa'], ['la', 'ces', 'si', 'ti']], [['tu'], ['ne'], ['ver', 'bo'], ['qui', 'dem'], ['vi', 'o', 'la', 'tus,'], ['ut'], ['au', 'da', 'ci', 'or'], ['quam'], ['ca', 'ti', 'li', 'na,'], ['fu', 'ri', 'o', 'si', 'or'], ['quam'], ['clo', 'di', 'us'], ['vi', 'de', 're', 're,'], ['ul', 'tro'], ['me'], ['ma', 'le', 'dic', 'tis'], ['la', 'ces', 'sis', 'ti,'], ['tu', 'am', 'que'], ['a'], ['me'], ['a', 'li', 'e', 'na', 'ti', 'o', 'nem'], ['com', 'men', 'da', 'ti', 'o', 'nem'], ['ti', 'bi'], ['ad'], ['im', 'pi', 'os'], ['ci', 'vis'], ['fo', 're'], ['pu', 'ta', 'vis', 'ti']]]
	assert preprocessor.syllabified() == correct

def test_u_to_v():
    # word begins with 'u'
    assert preprocessor.u_to_v("uita") == "vita"
    assert preprocessor.u_to_v("ultor") == "ultor"
    assert preprocessor.u_to_v("uae") == "vae"
    # word ends with 'u'
    assert preprocessor.u_to_v("auditu") == "auditu"
    assert preprocessor.u_to_v("arcu") == "arcu"
    # vowel + u + vowel
    assert preprocessor.u_to_v("amaui") == "amavi"
    # consonant + u + consonant
    assert preprocessor.u_to_v("amatus") == "amatus"
    # uu case 1
    assert preprocessor.u_to_v("uua") == "uva"
    # uu case 2
    assert preprocessor.u_to_v("uulnus") == "vulnus"
    # uu case 3
    assert preprocessor.u_to_v("uult") == "vult"
    # vowel + u + consontant
    assert preprocessor.u_to_v("auctor") == "auctor"
    # consonant + u + vowel
    assert preprocessor.u_to_v("habui") == "habui"
    assert preprocessor.u_to_v("habuerit") == "habuerit"
    assert preprocessor.u_to_v("imbuantur") == "imbuantur"
    # consonant + u + u + consonant
    assert preprocessor.u_to_v("tuus") == "tuus"
    assert preprocessor.u_to_v("mortuus") == "mortuus"
    assert preprocessor.u_to_v("perpetuum") == "perpetuum"
    assert preprocessor.u_to_v("fluuius") == "fluvius"
    assert preprocessor.u_to_v("exuuiae") == "exuviae"
    # consonant + u + vowel (not i)
    assert preprocessor.u_to_v("alueo") == "alveo"
    # consonant + u + vowel (i)
    assert preprocessor.u_to_v("inuitat") == "invitat"
    # consonantal i at start of word
    assert preprocessor.u_to_v("iuuenum") == "iuvenum"

def test_i_to_j():
    # initial i + consonant (not u/v)
    assert preprocessor.i_to_j("incoctus") == "incoctus"
    assert preprocessor.i_to_j("ignis") == "ignis"
    assert preprocessor.i_to_j("it") == "it"
    # initial i + vowel (not u/v)
    assert preprocessor.i_to_j("iaceo") == "jaceo"
    assert preprocessor.i_to_j("iecur") == "jecur"
    assert preprocessor.i_to_j("iocus") == "jocus"
    # initial i + u/v
    assert preprocessor.i_to_j("iubeo") == "jubeo"
    assert preprocessor.i_to_j("ius") == "jus"
    assert preprocessor.i_to_j("ivi") == "ivi"
