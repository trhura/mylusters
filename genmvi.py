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
    SIGN_ANUSVARA   + VOWEL_SIGN_U,
    VOWEL_SIGN_I    + VOWEL_SIGN_U,
    VOWEL_SIGN_E    + VOWEL_SIGN_AA,
    VOWEL_SIGN_E    + VOWEL_SIGN_AA + SIGN_ASAT,
]

TONES = [
    SIGN_DOT_BELOW,
    SIGN_VISARGA,
]

def main ():

    table = {}
    for m in MEDIALS:
        table[m] = {}
        for v in VOWELS:
            table[m][v] = False

    MEDIALS.reverse ()
    VOWELS.reverse ()

    with codecs.open ('syllables-more', 'r', 'utf8') as fil:
        for line in fil:
            line = line.strip ()
            if not line: continue

            medial = None
            for m in MEDIALS:
                if m in line:
                    medial = m
                    break
            if not medial: continue

            vowel  = None
            for v in VOWELS:
                if v in line:
                    vowel = v
                    break
            if not vowel: continue

            table[medial][vowel] = True

    with codecs.open ('mv-test-more.txt', 'w', 'utf8') as ofil:
        for m in sorted(MEDIALS):
            for v in sorted(VOWELS):
                ofil.write ('\t' + m + '\t+\t' + v + '\t=\t' + repr(table[m][v]) + '\n')

if __name__ == "__main__":
    main ()
