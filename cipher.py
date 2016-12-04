#!/usr/bin/env python3

from abc import ABC, abstractmethod
import utils

class AbstractCipher(ABC):

	@staticmethod
	@abstractmethod
	def encrypt(plaintext, key):
		"""Encrypts text given key"""

	@staticmethod
	@abstractmethod
	def decrypt(ciphertext, key):
		"""Decrypts text given key"""

	@staticmethod
	@abstractmethod
	def crack(ciphertext):
		"""Given text, it returns the most likely key and chi-square associated with it as a tuple"""

	@staticmethod
	@abstractmethod
	def usage():
		"""Prints usage of cipher, usually describing the key"""

	@staticmethod
	@abstractmethod
	def getNameOfCipher(key=None):
		"""Returns the name of the cipher.  If the key is provided, it will try to be more specific"""


class AbstractBruteForceCipher(AbstractCipher):

	@staticmethod
	def bruteForce(SubClass, ciphertext):
		"""Brute forces all the keys provided by SubClass"""

		bestKey = None
		lowestChi2 = 100000

		for key in SubClass.genKeys():
			maybePlaintext = SubClass.decrypt(ciphertext,key)
			chi2 = utils.calcChiSquared(maybePlaintext)

			if chi2 < lowestChi2:
				bestKey = key 
				lowestChi2 = chi2

		return (bestKey, lowestChi2)

	@staticmethod
	@abstractmethod
	def genKeys():
		"""Generates all possible keys to be tried"""
