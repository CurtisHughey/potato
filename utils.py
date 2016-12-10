#!/usr/bin/env python3

# General utilities used by multiple encryption algorithms

from collections import defaultdict
import unittest
import scipy
from scipy.stats import chisquare
from scipy.stats import chisqprob
from math import log10
import string

ALPHABET_SIZE = 26

_trigraphFreqData = None

# text must be lower case (otherwise ignored!)
def rot(text, shift):
    shiftedText = ""

    lowera = ord('a')

    for c in text:	
        d = ''
        if isAlpha(c):
            d = chr(((ord(c)-lowera+shift) % ALPHABET_SIZE)+lowera)
        else:
            d = c
        shiftedText += d

    return shiftedText

# Should really be called isLowerAlpha
def isAlpha(c):
    return ord('a') <= ord(c) <= ord('z')  # call tolower at somepoint for stream^^^^

def isPrintable(c):
    return c in string.printable  # But I eventually might want to do unicode...

def calcFreqs(text):
    counts = defaultdict(int)

    total = 0
    for c in text:
        if isAlpha(c):
            counts[c] += 1
            total += 1

    freqs = {}

    lowera = ord('a')
    for i in range(ALPHABET_SIZE):
        c = chr(lowera+i)

        if total == 0:
            freqs[c] = 0
        else:
            freqs[c] = counts[c] / total

    return (freqs, total)

def readExpectedFreqs(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

        freqs = dict()

        for line in lines:
            split = line.split()
            c = split[0]
            freq = float(split[1])
            freqs[c] = freq

        return freqs

def calcChiSquared(text):
    expectedFreqs = readExpectedFreqs('englishAlphaFreqs.txt')
    actualFreqs, total = calcFreqs(text)

    chiSquared = 0.0

    lowera = ord('a')
    for i in range(ALPHABET_SIZE):
        c = chr(lowera+i)
        chiSquared += ((actualFreqs[c]-expectedFreqs[c])**2) / expectedFreqs[c]

    chiSquared *= total  # Really, all the freqs above should've been multiplied by total, but this works out the same

    return chiSquared

# This doesn't currently work...
def isPlaintextWithConfidence(text, pVal):
    chi2 = calcChiSquared(text)
    print(chisqprob(chi2, ALPHABET_SIZE-1))
    return chisqprob(chi2, ALPHABET_SIZE-1) < pVal

# Copied from Wikipedia
def multInverse(a, n):
    t = 0 
    r = n
    newt = 1
    newr = a

    while newr != 0:
        quotient = r // newr
        (t, newt) = (newt, t-quotient*newt)
        (r, newr) = (newr, r-quotient*newr)

    if r > 1:
        raise ValueError('%d^-1 mod %d cannot be found' % (a,n))
    if t < 0:
        t = t+n

    return t

# Wih thanks to Practical Cryptography for the file: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/
# Note that we need to convert to lower-case and to freqs
# Also, you need to check to see if your trigraph is a key (wouldn't be added if freq is 0)
def readTrigraphFreqs(filename):
    global _trigraphFreqData

    if _trigraphFreqData != None:
        return _trigraphFreqData  # We're kind of caching it

    with open(filename, 'r') as f:
        lines = f.readlines()

        total = 0
        counts = dict()

        for line in lines:
            split = line.split()
            trigraph = split[0].lower()
            count = int(split[1])
            counts[trigraph] = count
            total += count

        freqs = dict()
        lowera = ord('a')
        for trigraph, count in counts.items():
            freqs[trigraph] = count / total

        _trigraphFreqData = (freqs, total)  # Saving for later as well

        return (freqs, total)

def calcTrigraphFitness(text):
    text = text.lower()  # Upper case characters should be allowed

    (freqs, total) = readTrigraphFreqs('data/english_trigrams.txt')

    # Now, we need to filter for only lower-case alphabet characters.  There could be some tweaking...
    strippedText = ''.join([c for c in text if isAlpha(c)])

    minLog = log10(0.01/total)  # We're basically giving a lower bound on the probability of a trigraph appearing
    
    fitness = 0
    for i in range(0, len(strippedText)-2):  # Iterating through trigraphs in text
        trigraph = strippedText[i:i+3]
        freq = freqs.get(trigraph, 0)  # 0 if not in the freqs
        if freq == 0:
            fitness += minLog
        else:
            fitness += log10(freq)

    return fitness/len(strippedText)  # We divide by the length to allow us to compare different text sizes...



class UtilTest(unittest.TestCase):
    def test_isAlpha(self):
        self.assertTrue(isAlpha('a'))
        self.assertTrue(isAlpha('z'))
        self.assertTrue(isAlpha('c'))
        self.assertFalse(isAlpha('1'))
        self.assertFalse(isAlpha('A'))

    def test_rot(self):
        self.assertEqual(rot('aaa', 2), 'ccc')
        self.assertEqual(rot('abc', 2), 'cde')
        self.assertNotEqual(rot('aaa', 2), 'ddd')
        self.assertEqual(rot('zzz', 2), 'bbb')
        self.assertEqual(rot('xyz', 2), 'zab')
        self.assertEqual(rot('a c', 2), 'c e')
        self.assertEqual(rot('a1c', 2), 'c1e')
        self.assertEqual(rot('aAc', 2), 'cAe')

    def test_calcFreqs(self):
        freqs, _ = calcFreqs('abca')
        self.assertAlmostEqual(freqs['a'], 0.5)
        self.assertAlmostEqual(freqs['b'], 0.25)
        self.assertAlmostEqual(freqs['z'], 0.0)

    def test_readExpectedFreqs(self):
        freqs = readExpectedFreqs('englishAlphaFreqs.txt')
        self.assertEqual(freqs['c'], 0.02782)
        self.assertEqual(freqs['z'], 0.00074)        

    def test_calcChiSquared(self):
        x2 = calcChiSquared('this should be a valid english text, and so the p value should be fairly low, hopefully.')
        self.assertAlmostEqual(x2, 39.515306094)

        x2 = calcChiSquared('abcdefghijklmnopqrstuvwxyz')
        self.assertAlmostEqual(x2, 148.894749139)

    def test_multInverse(self):
        self.assertEqual(multInverse(7,26), 15)
        self.assertEqual(multInverse(8953851,26), 17)
        self.assertEqual(multInverse(1,26), 1)
        with self.assertRaises(ValueError):
            multInverse(13,26)

