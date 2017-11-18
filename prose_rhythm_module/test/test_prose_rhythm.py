from prose_rhythm_module import prose_rhythm_scanner

TEST_TEXT = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec vero necesse est quemquam a me nominari; vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me alienationem commendationem tibi ad impios civis fore putavisti."
ALL_TRUE_CONFIG = prose_rhythm_scanner.prose_rhythm(elision=True, sests=True, mute_plus_liquid=True, punctuation=[':', ';', '.', '?', '!'], text=TEST_TEXT)

def test_preprocessed_text():
	CORRECT = ['[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit hostis, qui non bellum eodem tempore mihi quoque indixerit', 'Nec vero necesse est quemquam a me nominari', 'vobiscum ipsi recordamini', 'Mihi poenarum illi plus, quam optaram, dederunt', 'te miror, Antoni, quorum facta imitere, eorum exitus non perhorrescere', 'Atque hoc in aliis minus mirabar', 'Nemo enim illorum inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti', 'Tu ne verbo quidem violatus, ut audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me alienationem commendationem tibi ad impios civis fore putavisti']
	assert ALL_TRUE_CONFIG.preprocessed_text() == CORRECT

def test_syllabified():
	CORRECT = [[['quo', 'nam'], ['me', 'o'], ['fa', 'to,'], ['pa', 'tres'], ['con', 'scrip', 'ti,'], ['fi', 'e', 'ri'], ['di', 'cam,'], ['ut'], ['ne', 'mo'], ['his'], ['an', 'nis'], ['vi', 'gin', 'ti'], ['rei'], ['pu', 'bli', 'cae'], ['fu', 'e', 'rit'], ['hos', 'tis,'], ['qui'], ['non'], ['bel', 'lum'], ['e', 'o', 'dem'], ['tem', 'po', 're'], ['mi', 'hi'], ['quo', 'que'], ['in', 'di', 'xe', 'rit']], [['nec'], ['ve', 'ro'], ['ne', 'ces', 'se'], ['est'], ['quem', 'quam'], ['a'], ['me'], ['no', 'mi', 'na', 'ri']], [['vo', 'bis', 'cum'], ['ip', 'si'], ['re', 'cor', 'da', 'mi', 'ni']], [['mi', 'hi'], ['poe', 'na', 'rum'], ['il', 'li'], ['plus,'], ['quam'], ['op', 'ta', 'ram,'], ['de', 'de', 'runt']], [['te'], ['mi', 'ror,'], ['an', 'to', 'ni,'], ['quo', 'rum'], ['fac', 'ta'], ['i', 'mi', 'te', 're,'], ['e', 'o', 'rum'], ['ex', 'i', 'tus'], ['non'], ['per', 'hor', 'res', 'ce', 're']], [['at', 'que'], ['hoc'], ['in'], ['a', 'li', 'is'], ['mi', 'nus'], ['mi', 'ra', 'bar']], [['ne', 'mo'], ['e', 'nim'], ['il', 'lo', 'rum'], ['in', 'i', 'mi', 'cus'], ['mi', 'hi'], ['fu', 'it'], ['vo', 'lun', 'ta', 'ri', 'us,'], ['om', 'nes'], ['a'], ['me'], ['rei'], ['pu', 'bli', 'cae'], ['cau', 'sa'], ['la', 'ces', 'si', 'ti']], [['tu'], ['ne'], ['ver', 'bo'], ['qui', 'dem'], ['vi', 'o', 'la', 'tus,'], ['ut'], ['au', 'da', 'ci', 'or'], ['quam'], ['ca', 'ti', 'li', 'na,'], ['fu', 'ri', 'o', 'si', 'or'], ['quam'], ['clo', 'di', 'us'], ['vi', 'de', 're', 're,'], ['ul', 'tro'], ['me'], ['ma', 'le', 'dic', 'tis'], ['la', 'ces', 'sis', 'ti,'], ['tu', 'am', 'que'], ['a'], ['me'], ['a', 'li', 'e', 'na', 'ti', 'o', 'nem'], ['com', 'men', 'da', 'ti', 'o', 'nem'], ['ti', 'bi'], ['ad'], ['im', 'pi', 'os'], ['ci', 'vis'], ['fo', 're'], ['pu', 'ta', 'vis', 'ti']]]
	assert ALL_TRUE_CONFIG.syllabified() == CORRECT

def test_long_by_nature():
	SAMPLE_SYLLABLE_SHORT = 'me'
	SAMPLE_SYLLABLE_LONG_VOWEL = 'trēs'
	SAMPLE_SYLLABLE_DIPHTHONG = 'tae'
	assert ALL_TRUE_CONFIG.long_by_nature(SAMPLE_SYLLABLE_SHORT) == False, "syllable has short vowel"
	assert ALL_TRUE_CONFIG.long_by_nature(SAMPLE_SYLLABLE_LONG_VOWEL) == True, "syllable has long vowel"
	assert ALL_TRUE_CONFIG.long_by_nature(SAMPLE_SYLLABLE_DIPHTHONG) == True, "syllable has diphthong`"
