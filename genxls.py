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
    VOWEL_SIGN_U + SIGN_ANUSVARA ,
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

            # Bugs
            line = line.replace (u'\u102B', u'\u102C')

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
            if vowel: table[consonant][medial].setdefault(vowel, {})

            tone = None
            for t in TONES:
                if t in line:
                    tone = t
                    break
            if tone: table[consonant][medial][vowel].setdefault(tone, {})

    workbook = xlwt.Workbook ('utf-8')
    worksheet = workbook.add_sheet ("Grapheme Clusters")

    VMR = len(TONES)            # VOWEL ROW SPAN RANGE
    MMR = len(VOWELS)  * VMR    # MEDIALS ROW SPAN RANGE
    CMR = len(MEDIALS) * MMR    # CONSONANT ROW SPAN RANGE

    default_style = xlwt.easyxf ('alignment:vertical top;'
                                 'borders: left thick;'
                                 'borders: right thick;'
                                 'borders: top thick;'
                                 'borders: bottom thick;')

    invalid_style = xlwt.easyxf ('alignment:vertical top;'
                                 'font: color gray25;'
                                 'font: struck_out True')

    empty_medial_style = xlwt.easyxf ('pattern: pattern solid;'
                                      'borders: left thick;'
                                      'borders: right thick;'
                                      'borders: top thick;'
                                      'borders: bottom thick;'
                                      'pattern: fore_color gray25')

    header_style  = xlwt.easyxf ('alignment:vertical top;'
                                 'borders: left thick;'
                                 'borders: right thick;'
                                 'borders: top thick;'
                                 'borders: bottom thick;'
                                 'font: bold True;'
                                 'font: shadow True;'
                                 'font: height 300;')

    for i, heading in enumerate (['Consonants', 'Medials', 'Vowels', 'Tones']):
        worksheet.write (0, i, heading, header_style)

    worksheet.panes_frozen = True
    worksheet.horz_split_pos = 1

    def uni_repr (string):
        utf_repr = u' '.join ([repr(c)[3:-1] for c in string]).replace ("u", "U+").upper ()
        return string + ' (' + utf_repr + ')'

    for i, consonant in enumerate(sorted(table.keys())):
        worksheet.write_merge ((CMR*i)+1, CMR+(CMR*i),
                               0, 0,
                               uni_repr(consonant),
                               default_style)

        for j, medial in enumerate(sorted(MEDIALS)):
            style = default_style
            if not table[consonant].has_key (medial):
                style = invalid_style

            worksheet.write_merge ((CMR*i)+(MMR*j)+1, (CMR*i)+(MMR*j)+MMR,
                                   1, 1,
                                   uni_repr(consonant + medial) if medial else '',
                                   style if medial else empty_medial_style)

            for k, vowel in enumerate(sorted(VOWELS)):
                style = default_style
                if  not (table[consonant].has_key (medial) and \
                    table[consonant][medial].has_key (vowel)):
                    style = invalid_style

                worksheet.write_merge ((CMR*i)+(MMR*j)+(VMR*k)+1, (CMR*i)+(MMR*j)+(VMR*k)+VMR,
                                       2, 2,
                                       uni_repr(consonant + (medial if medial else '') + vowel),
                                       style)

                for l, tone in enumerate (TONES):
                    style = default_style
                    if  not (table[consonant].has_key (medial) and \
                            table[consonant][medial].has_key (vowel) and \
                            table[consonant][medial][vowel].has_key (tone)):
                        style = invalid_style

                    worksheet.write ((CMR*i)+(MMR*j)+(VMR*k)+l+1,
                                     3,
                                     uni_repr(consonant + (medial if medial else '') + vowel + tone), style)


    for i in range (1, CMR * len(table.keys()), 1):
        if (i - 1) % CMR == 0:
            continue
        worksheet.row(i).level = 1
        worksheet.row(i).hidden = True
        worksheet.row(i).collapse = True

        if (i - 1) % MMR == 0:
            continue
        worksheet.row(i).level = 2
        worksheet.row(i).hidden = True
        worksheet.row(i).collapse = True

    worksheet.col(0).width = 20 * 256
    worksheet.col(1).width = 30 * 256
    worksheet.col(2).width = 40 * 256
    worksheet.col(3).width = 50 * 256

    import itertools
    try:
        for i in itertools.count ():
            worksheet.row(i).height = 3 * 256
            worksheet.row(i).height_mismatch = 1
    except:
        pass


    workbook.save ('clusters.xls')

if __name__ == "__main__":
    main ()
