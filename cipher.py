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


class AbstractBruteForceCipher(AbstractCipher):

	def bruteForce(self, ciphertext):
		"""Brute forces all the keys provided by SubClass"""

		bestKey = None
		lowestChi2 = 100000

		for key in self.genKeys():  # genKeys and decrypt are the subclass functions
			maybePlaintext = self.decrypt(ciphertext,key)
			chi2 = utils.calcChiSquared(maybePlaintext)

			if chi2 < lowestChi2:
				bestKey = key 
				lowestChi2 = chi2

		return (bestKey, lowestChi2)

	@abstractmethod
	def genKeys(self):
		"""Generates all possible keys to be tried"""
