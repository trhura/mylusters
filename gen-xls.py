#! /usr/bin/env python
# -*- coding: utf-8 -*-

from myanmar.language import *

import xlwt
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
           None,
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

def unicode_repr (char):
    return repr(char)[3:-1].upper()

def main ():
    table = {}
    MEDIALS.reverse ()
    VOWELS.reverse ()

    with codecs.open ('syllables', 'r', 'utf8') as fil:
        for line in fil:
            line = line.strip ()
            if not line: continue

            consonant = line[0]
            table.setdefault (consonant, {})

            medial = None
            for m in MEDIALS:
                if m and m in line:
                    medial = m
                    break
            table[consonant].setdefault (medial, {})

            vowel = None
            for v in VOWELS:
                if v in line:
                    vowel = v
                    break
            table[consonant][medial].setdefault(vowel, {})

            tone = None
            for t in TONES:
                if t in line:
                    tone = t
                    break
            table[consonant][medial][vowel].setdefault(tone, {})

    import pprint
    with codecs.open ("test.txt", 'w') as ofile:
        ofile.write (pprint.pformat(table))

    workbook = xlwt.Workbook ('utf-8')
    worksheet = workbook.add_sheet ("Grapheme Clusters")

    VMR = len(TONES)            # VOWEL ROW SPAN RANGE
    MMR = len(VOWELS)  * VMR    # MEDIALS ROW SPAN RANGE
    CMR = len(MEDIALS) * MMR    # CONSONANT ROW SPAN RANGE

    for i, consonant in enumerate(table.keys()):
        worksheet.write_merge ((CMR*i), CMR+(CMR*i)-1,
                               0, 0,
                               consonant,
                               xlwt.easyxf (
                                   'alignment:vertical top;'
                                   ))

        for j, medial in enumerate(MEDIALS):
            worksheet.write_merge ((CMR*i)+(MMR*j), (CMR*i)+(MMR*j)+MMR-1,
                                   1, 1,
                                   unicode(medial),
                                   xlwt.easyxf (
                                       'alignment:vertical top;'
                                       ))
            #if table[consonant].has_key (medial):

            for k, vowel in enumerate(VOWELS):
                worksheet.write_merge ((CMR*i)+(MMR*j)+(VMR*k), (CMR*i)+(MMR*j)+(VMR*k)+VMR-1,
                                       2, 2,
                                       vowel)

                for l, tone in enumerate (TONES):
                    worksheet.write ((CMR*i)+(MMR*j)+(VMR*k) + l,
                                     4,
                                     tone)

    workbook.save ('clusters.xls')

if __name__ == "__main__":
    main ()
