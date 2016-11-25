#!/usr/bin/env python3

# General utilities used by multiple encryption algorithms

from collections import defaultdict
import unittest

# text must be lower case!
def rot(text, shift):
    shiftedText = ""

    lowera = ord('a')

    for c in text:	
        shiftedC = chr(((ord(c)-lowera+shift) % 26)+lowera)
        shiftedText += shiftedC

    return shiftedText

def isAlpha(c):
    return ord('a') <= ord(c) <= ord('z')

def calcFreqs(text):
    counts = defaultdict(int)

    total = 0
    for c in text:
        if isAlpha(c):
            counts[c] += 1
            total += 1

    freqs = defaultdict(int)

    for c in counts.keys():
        freqs[c] = counts[c] / total

    return freqs


def calcChiSquared(text, expectedFreqs):
    actualFreqs = calcFreqs(text)

    chiSquared = 0.0

    lowera = ord('a')
    for i in range(26):
        c = chr(lowera+i)
        chiSquared += ((actualFreqs[c]-expectedFreqs[c])**2) / expectedFreqs[c]

    return chiSquared

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

    def test_calcFreqs(self):
        freqs = calcFreqs('abca')
        self.assertAlmostEqual(freqs['a'], 0.5)
        self.assertAlmostEqual(freqs['b'], 0.25)
        self.assertAlmostEqual(freqs['z'], 0.0)

    def test_readExpectedFreqs(self):
        freqs = readExpectedFreqs('englishAlphaFreqs.txt')
        self.assertEqual(freqs['c'], 0.02782)
        self.assertEqual(freqs['z'], 0.00074)

    def test_calcChiSquared(self):
        freqs = readExpectedFreqs('englishAlphaFreqs.txt')
        self.assertAlmostEqual(calcChiSquared('abc', freqs), 11.801833324)
