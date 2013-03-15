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

def main ():

    table = {}

    with codecs.open ('syllables', 'r', 'utf8') as fil:
        for line in fil:
            line = line.strip ()

            if not line:
                continue

            consonant = line[0]

            if not table.has_key (consonant):
                table[consonant] = {}

            rev_medials = list(MEDIALS)
            rev_medials.reverse ()

            for medial in rev_medials:
                if not table[consonant].has_key (medial):
                    table[consonant][medial] = False

                if medial in line:
                    table[consonant][medial] = True
                    break
            # else:
            #     print line

    output = ''
    keys = table.keys ()
    keys.sort ()

    output +=  ',' + ",".join (MEDIALS) + '\n'

    def unicode_repr (char):
        return repr(char)[3:-1].upper()

    for consonant in keys:
        output += consonant + '\t(' + unicode_repr(consonant) + ')'
        for medial in MEDIALS:
            if table[consonant][medial]:
                output += ',' + consonant + medial
            else:
                output += ', '
        output += '\n'

    with codecs.open ('CM.csv','w', 'utf8') as ofil:
        ofil.write (output)

if __name__ == "__main__":
    main ()
