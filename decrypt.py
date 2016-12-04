#!/usr/bin/env python3

# TODO
# Vigenere (get Beaufort)
# XOR
# Playfair
# Monoalphabetic
# RC4
# Transposition
# Substitution


import sys
import getopt
import nothing
import affine
import vigenere
import unittest

 # Would be cool to dynamically update this list
ciphers = [
            nothing.Nothing
          , affine.Affine
          , vigenere.Vigenere
          ] 

def main(argv):
    ciphertext = ''

    if (len(argv) < 2):
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv,"hc:")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-c':
            ciphertext = arg

    findCipherAndDecrypt(ciphertext)

def usage():
    print('Usage: ./decrypt.py -c <ciphertext>')

# Eventually, I'll have to do something in case the entered text is all caps^^^
# Unit test...^^^
def findCipherAndDecrypt(ciphertext):

    lowestChi2 = 100000
    bestCipher = None
    bestKey = None

    print('Decrypting %s' % ciphertext)

    print('------------------------------------------------------------------------')
    print('Type of Cipher                | Key                  | Chi-Squared Value')
    print('------------------------------------------------------------------------')

    for cipher in ciphers:
        key, chi2 = cipher.crack(ciphertext)
        print('%-30s| %-21s| %.4f' % (cipher.getNameOfCipher(key), str(key), chi2))

        if (chi2 < lowestChi2):
            lowestChi2 = chi2
            bestCipher = cipher
            bestKey = key 

    print('\n')

    plaintext = bestCipher.decrypt(ciphertext, bestKey)
    print('----------')
    print('Best cipher was: %s' % bestCipher.getNameOfCipher(bestKey))
    print('Decrypted text:')
    print(plaintext)

    return (plaintext, bestCipher, bestKey, lowestChi2)

if __name__ == '__main__':
    main(sys.argv[1:])


class DecryptTest(unittest.TestCase):    

    def test_findCipherAndDecrypt(self):
        tests = [ 
                  ( 'hello there lets see if this gets encrypted or not by affine.'
                  , 'qbkkz yqbob kbyt tbb vg yqvt lbyt buroxeybw zo uzy mx hggvub.'
                  , affine.Affine
                  , (5, 7)
                  )
                , ( 'this should just be regular plaintext, and not messed with at all.'
                  , 'this should just be regular plaintext, and not messed with at all.'
                  , nothing.Nothing
                  , None
                  )
                , ('cryptographyisthepracticeandstudyoftechniquesforsecurecommunicationinthepresenceofthirdpartiescalledadversariesmoregenerallyitisaboutconstructingandanalyzingprotocolsthatovercometheinfluenceofadversariesandwhicharerelatedtovariousaspectsininformationsecuritysuchasdataconfidentialitydataintegrityauthenticationandnonrepudiationmoderncryptographyintersectsthedisciplinesofmathematicscomputerscienceandelectricalengineeringmoderncryptographyisheavilybasedonmathematicaltheoryandcomputersciencepracticecryptographicalgorithmsaredesignedaroundcomputationalhardnessassumptionsmakingsuchalgorithmshardtobreakinpracticebyanyadversaryitistheoreticallypossibletobreaksuchasystembutitisinfeasibletodosobyanyknownpracticalmeanscryptologyrelatedtechnologyhasraisedanumberoflegalissuestheelectronicfrontierfoundationwasinvolvedinacaseintheunitedstateswhichquestionedwhetherrequiringsuspectedcriminalstoprovidetheirdecryptionkeystolawenforcementisunconstitutionaltheeffarguedthatthisisaviolationoftherightofnotbeingforcedtoincriminateoneselfasgiveninthefifthamendm'
                  , 'ulpkxwrjugccqdlbvkvinlctzevoknlycwqlytcrqbmyjaszdwwlmikzeglimkllcfimvezygmiapfwvjjbsalukezeayjxetwwxryzmckuidiaxglvbivpjucgcqeamrwsceuienxzfunzikiyvuevpgkahxkvwegwfgwbssnfqiznggvolmtfzcpivnwiwvhdpjmrmmmdshurlqnzuizvmwsnvyxwgslzjyalkjvxxatfceaszxsnzjrapuoidxgdmwyvwlllutjrntvyeomiwanpyeblahkzkztlsrpxppfnzxebtghrihvzflvkyltsnzjruzvyiigzjhnfbviazszixmckytowbswxzngqadcezwwqeukciullctngwxhokzvanayexiiyvyczgbcawrgivrahvzvqyygfyizyulpkxwrjugccqdzyrqmtjtujzhwyeukciullctvpbswiitevouidkybpjmtdivnwjivgbtuytmcxegaivtptuucbsztlbdnezpvyjdkvpvuijyvouidkybllcfietssluiiadsmjpqxeaienqivahxnykssfxjvqezgjcezolismiivahgmekeawvwciyquuqizdslpdxqdlbvjvmeawrgpgagmjdftplismiivkotceajknvhfceanznmvqwujdftpliujwwmquetovzohgmekeawrgqmlfmtmcxegffbczpdukzhbpubejpwrqbrnvitkyuvrcxtyijjtpyucdwafwmkcimwwwkmsvtuzijrbtwlwjyvosnzjrelkceqstgwxzieklkyzixppmhzoildlukzwesawylymdlcfiilhzykcizcwkldvqyymlntmnlyuxvqxahrgwbzhlfqmlplbvdvlpulpkxqzfevtwbzdunzrnzjwvhiveamligwyknzoybtghrgxppwzwvvofwxkcebezcjdwigaicvxqzfiwolmcaayosnygnszmvrxiixilegcexvqxahroiwywmvgjidycmzrqylbvamnezudzrlx'
                  , vigenere.Vigenere
                  , 'surveil'
                  )
                ]

        for (plaintext, ciphertext, cipherType, key) in tests:
            (maybePlaintext, bestCipher, bestKey, _) = findCipherAndDecrypt(ciphertext)
            self.assertEqual((plaintext, cipherType, key), (maybePlaintext, bestCipher, bestKey))
