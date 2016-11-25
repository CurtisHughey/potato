# General utilities used by multiple encryption algorithms

from collections import defaultdict

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

    chiSquares = 0.0

    lowera = ord('a')
    for i in range(0, 25)
        c = chr(lowera+i)
        output += ((expectedFreqs[c]-actualFreqs[c])**2) / 2

    return output

def readExpectedFreqs(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

        freqs = dict()

        for line in lines:
            split = line.split()
            c = split[0]
            freq = float(split[1])
            freqs[c] = freq

        print(freqs)

        return freqs

