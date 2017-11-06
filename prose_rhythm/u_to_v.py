"""
Convert U to V
Rules:
vowel + u = v (except au, which is a diphthong.
consonant + u = u
consonant + u + u + consonant = both u's are vowels
consonant + u + u + vowel = first u is V, second stays u

Rules for at the start of words:
u + consonant = u
u + vowel = v
"""

VOWELS = ["a", "e", "i", "o", "u"]

def convert_u_to_v(word):
    """
    Convert u in word to v.
    :param word: string
    :return: string
    """
    word = list(word.lower())

    # u at beginning of the word
    if word[0] == "u" and word[1] in VOWELS:
        word[0] = "v"

    # u in word
    for char in word:
        char_index = word.index(char)
        if char_index != len(word) - 1 and char == "u":
            # vowel preceeds u and vowel follows
            if len(word) > 2 and word[char_index - 1] in VOWELS and word[char_index + 1] in VOWELS:
                    word[char_index] = "v"
            # consonant + u + u + vowel
            if len(word) > 3 and word[char_index - 1] not in VOWELS and word[char_index + 1] == "u" and word[char_index + 2] in VOWELS:
                    word[char_index + 1] = "v"

    return "".join(word)

if __name__ == "__main__":
    tests1 = ["amaui", "amatus", "auctor", "habui", "habuerit", "imbuantur", "fluuius", "exuuiae", "uita", "uae",
              "mortuus", "perpetuum"]
    tests2 = ["suo", "amaui", "curam", "sollicitudinem", "tuam", "cum", "audisses", "petiturum", "suasisti", "dum",
              "putas", "insalubres", "grauis", "Tuscorum", "litus", "extenditur", "procul", "recesserunt",
              "saluberrimo", "monitum", "subiacent", "ut", "metum", "situm", "uillae", "auditu", "relatu", "iucunda",
              "erunt", "Caelum", "frigidum", "gelidum", "asiduo", "laetantur", "asperantur", "respuit", "laurum",
              "patitur", "interdum", "saepius", "sub", "urbe", "spiritu", "aliquo", "mouetur", "frequentius", "auras",
              "uentos", "multi:", "uideas", "auos", "proauosque", "iuuenum", "audias", "fabulas", "ueteres",
              "sermonesque", "maiorum", "cumque", "ueneris", "natum", "pulcherrima", "amphitheatrum", "immensum",
              "rerum", "natura", "diffusa", "montibus", "cingtur", "summa", "sui", "antiqua", "frequens", "uaria",
              "uenatio", "caeduae", "siluae", "descendunt", "pingues", "terrenique", "usquam", "saxum", "quaeratur",
              "occurit", "cedunt", "serius", "tantum", "minus", "percoquunt", "sub", "latus", "uineae", "porriguntur",
              "unamque", "lateque", "contexerunt", "quarum", "imoque", "quasi", "arbusta", "nascuntur", "campique",
              "quos", "boues", "perfringunt", "tenacissimum", "solum", "cum", "primum", "prosecatur", "adsurgit", "ut",
              "demum", "sulco", "perdometur", "trifolium", "quasi", "nouas", "alunt", "cuncta", "perennibus", "riuis",
              "nutriuntur", "ubi", "aquae", "plurimum", "palus", "nulla", "quia", "deuexa", "quidquid", "liquoris",
              "absorbuit", "effundit", "nauium", "omnesque", "urbem", "dumtaxat", "uere", "summittitur", "immensiosque",
              "fluminis", "alueo", "autumno", "resumit-", "uoluptatem", "situm", "aliquam", "pulchritudinem",
              "uideberis", "uarietate", "quocumque", "oculi", "reficientur", "uilla", "quasi", "summo", "leuiter",
              "cliuo", "consurgit", "ut", "cum", "putes", "Appenninum", "longius", "quamlibet", "sui", "aestiuumque",
              "quasi", "inuitat", "in", "porticum", "ueterum"]

    # print(convert_u_to_v("amaui"))


    for test in tests2:
        print("Word to test: " + test + "       Result: ", convert_u_to_v(test))
