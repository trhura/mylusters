#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

    with codecs.open ('syllables', 'r', 'utf8') as fil:
        for line in fil:
            line = line.strip ()

            if not line:
                continue

            brk = False
            for medial in MEDIALS:
                if medial in line:
                    brk = True
            if brk:
                continue

            consonant = line[0]

            if not table.has_key (consonant):
                table[consonant] = {}

            rev_vowels = list(VOWELS)
            rev_vowels.reverse ()

            for vowel in rev_vowels:
                if not table[consonant].has_key (vowel):
                    table[consonant][vowel] = False

                if vowel in line:
                    table[consonant][vowel] = {}
                    for tone in TONES:
                        if tone in line:
                            table[consonant][vowel][tone] = True

                    break
            # else:
            #     print line
    def unicode_repr (char):
        return repr(char)[3:-1].upper()

    output = ''
    keys = table.keys ()
    keys.sort ()

    output += ',' + ",".join (TONES) + '\n'

    for consonant in keys:
        for vowel in VOWELS:
            if table[consonant][vowel]:
                output += consonant + vowel
                for tone in TONES:
                    if table[consonant][vowel].has_key(tone):
                        output += ',' + consonant + vowel + tone
                    else:
                        output += ', '
                output += '\n'

    with codecs.open ('CVT.csv','w', 'utf8') as ofil:
        ofil.write (output)

if __name__ == "__main__":
    main ()
