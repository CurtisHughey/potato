#!/usr/bin/env python3

# TODO
# Affine (get Caesar, Atbash)
# Vigenere (get Beaufort)
# XOR
# Playfair
# Monoalphabetic
# RC4
# Transposition
# Substitution


import sys, getopt
import affine

ciphers = [affine.Affine]  # Would be cool to dynamically update this list

def main(argv):
    ciphertext = ''

    if (len(argv) < 1):
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

def findCipherAndDecrypt(ciphertext):

    lowestChi2 = 100000
    bestCipher = None
    bestKey = None

    print('Type of Cipher     | Key             | Chi-Squared Value')
    print('--------------------------------------------------------')

    for cipher in ciphers:
        key, chi2 = cipher.crack(ciphertext)
        print('%-19s| %-16s| %.4f' % (cipher.getNameOfCipher(key), str(key), chi2))

        if (chi2 <= lowestChi2):
            lowestChi2 = chi2
            bestCipher = cipher
            bestKey = key 

    print('\n')

    plaintext = cipher.decrypt(ciphertext, key)
    print('----------')
    print('Best cipher was: %s' % cipher.getNameOfCipher(key))
    print('Decrypted text:')
    print(plaintext)

if __name__ == '__main__':
    main(sys.argv[1:])

