from myanmar.language import *
import codecs

MEDIALS = [CONSONANT_SIGN_MEDIAL_YA,
           CONSONANT_SIGN_MEDIAL_RA,
           CONSONANT_SIGN_MEDIAL_WA,
           CONSONANT_SIGN_MEDIAL_HA,
           CONSONANT_SIGN_MEDIAL_YA + CONSONANT_SIGN_MEDIAL_WA,
           CONSONANT_SIGN_MEDIAL_RA + CONSONANT_SIGN_MEDIAL_WA,
           CONSONANT_SIGN_MEDIAL_YA + CONSONANT_SIGN_MEDIAL_HA,
           CONSONANT_SIGN_MEDIAL_RA + CONSONANT_SIGN_MEDIAL_HA,
           CONSONANT_SIGN_MEDIAL_WA + CONSONANT_SIGN_MEDIAL_HA,
#           CONSONANT_SIGN_MEDIAL_YA + CONSONANT_SIGN_MEDIAL_WA + CONSONANT_SIGN_MEDIAL_HA,
           CONSONANT_SIGN_MEDIAL_RA + CONSONANT_SIGN_MEDIAL_WA + CONSONANT_SIGN_MEDIAL_HA,
           ]

VOWELS = [
    VOWEL_SIGN_AA,
    VOWEL_SIGN_I,
    VOWEL_SIGN_II,
    VOWEL_SIGN_U,
    VOWEL_SIGN_UU,
    VOWEL_SIGN_E,
    VOWEL_SIGN_AI,
    SIGN_ANUSVARA,
    VOWEL_SIGN_U + SIGN_ANUSVARA ,
    VOWEL_SIGN_I + VOWEL_SIGN_U,
    VOWEL_SIGN_E + VOWEL_SIGN_AA,
    VOWEL_SIGN_E + VOWEL_SIGN_AA + SIGN_ASAT,
]

TONES = [
    SIGN_DOT_BELOW,
    SIGN_VISARGA,
]

def main ():

    table = {}
    for v in VOWELS:
        table[v] = {}
        for d in TONES:
            table[v][d] = False

    #MEDIALS.reverse ()
    VOWELS.reverse ()

    with codecs.open ('alls', 'r', 'utf8') as fil:
        for line in fil:
            line = line.replace (u'\u102B', u'\u102C')
            line = line.strip ()
            if not line: continue

            for vowel in VOWELS:
                if vowel in line:
                    try:
                        tone = line[line.find (vowel) + len(vowel)]
                        if tone in TONES:
                            table[vowel][tone] = True
                    except:
                        continue

    def uni_repr (string):
        utf_repr = u' '.join ([repr(c)[3:-1] for c in string]).replace ("u", "U+").upper ()
        return string + '\t(' + utf_repr + ')'

    with codecs.open ('vd-combinations.txt', 'w', 'utf8') as ofil:
        for v in sorted(VOWELS):
            for d in sorted(TONES):
                ofil.write ((u'\u2713' if table[v][d] else u'\u2716') + '\t' +
                            uni_repr(v) + '\t+\t' + uni_repr(d) + '\n')

if __name__ == "__main__":
    main ()
