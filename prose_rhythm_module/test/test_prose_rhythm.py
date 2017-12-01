"""
Unit tests for Prose_Rhythm_Scanner class.
"""

from prose_rhythm_module.prose_rhythm_scanner import Prose_Rhythm_Scanner

TEST_TEXT = "[1] [I] Quonam meo fato, patres conscripti, fieri dicam, ut nemo his annis viginti rei publicae fuerit " \
            "hostis, qui non bellum eodem tempore mihi quoque indixerit? Nec vero necesse est quemquam a me nominari; " \
            "vobiscum ipsi recordamini. Mihi poenarum illi plus, quam optaram, dederunt: te miror, Antoni, quorum " \
            "facta imitere, eorum exitus non perhorrescere. Atque hoc in aliis minus mirabar. Nemo enim illorum " \
            "inimicus mihi fuit voluntarius, omnes a me rei publicae causa lacessiti. Tu ne verbo quidem violatus, ut " \
            "audacior quam Catilina, furiosior quam Clodius viderere, ultro me maledictis lacessisti, tuamque a me " \
            "alienationem commendationem tibi ad impios civis fore putavisti."

def test_long_by_nature():
    scanner = Prose_Rhythm_Scanner(elision=False, sests=False, mute_plus_liquid=False, text=TEST_TEXT,
                                   punctuation=['.'])
    # long by nature
    assert scanner.long_by_nature('ī') == True
    assert scanner.long_by_nature('ae') == True
    assert scanner.long_by_nature('bī') == True
    assert scanner.long_by_nature('īm') == True
    assert scanner.long_by_nature('mae') == True
    assert scanner.long_by_nature('aen') == True
    # not long by nature
    assert scanner.long_by_nature('o') == False
    assert scanner.long_by_nature('bo') == False
    assert scanner.long_by_nature('ik') == False