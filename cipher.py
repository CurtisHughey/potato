#!/usr/bin/env python3

from abc import ABC, abstractmethod
import utils

class AbstractCipher(ABC):

	@abstractmethod
	def encrypt(self, plaintext, key):
		"""Encrypts text given key"""

	@abstractmethod
	def decrypt(self, ciphertext, key):
		"""Decrypts text given key"""

	@abstractmethod
	def crack(self, ciphertext):
		"""Given text, it returns the most likely key and chi-square associated with it as a tuple"""

	@abstractmethod
	def usage(self):
		"""Prints usage of cipher, usually describing the key"""

	@abstractmethod
	def getNameOfCipher(self, key=None):
		"""Returns the name of the cipher.  If the key is provided, it will try to be more specific"""
		
	# This requires better explanation
	def onlyLowerCase(self):
		return True  # By default
		"""Returns boolean, whether it can only be lower case (e.g. Vigenere), or anything (xor)"""


class AbstractBruteForceCipher(AbstractCipher):

	def bruteForce(self, ciphertext, minReadRate=0.4):
		"""Brute forces all the keys provided by SubClass.  minReadRate enforces minimum rate of readable chars"""

		bestKey = None
		lowestChi2 = 100000

		if self.onlyLowerCase():
			ciphertext = ciphertext.lower()

		for key in self.genKeys():  # genKeys and decrypt are the subclass functions

			maybePlaintext = self.decrypt(ciphertext,key)

			if minReadRate > 0.0:
				readPerc = len([c for c in maybePlaintext if utils.isAlpha(c)]) / len(maybePlaintext)
				if readPerc < minReadRate:
					continue

			chi2 = utils.calcChiSquared(maybePlaintext)

			if chi2 < lowestChi2:
				bestKey = key 
				lowestChi2 = chi2

		#print(utils.calcTrigraphFitness(self.decrypt(ciphertext, bestKey)))		

		return (bestKey, lowestChi2)

	@abstractmethod
	def genKeys(self):
		"""Generates all possible keys to be tried"""
