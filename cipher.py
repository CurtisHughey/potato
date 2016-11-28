#!/usr/bin/env python3

from abc import ABC, abstractmethod

class AbstractCipher(ABC):

	@staticmethod
	@abstractmethod
	def encrypt(text, key):
		"""Encrypts text given key"""
		pass

	@staticmethod
	@abstractmethod
	def decrypt(text, key):
		"""Decrypts text given key"""
		pass

	@staticmethod
	@abstractmethod
	def crack(text):
		"""Given text, it returns the most likely key and chi-square associated with it as a tuple"""
		pass

	@staticmethod
	@abstractmethod
	def usage():
		"""Prints usage of cipher, usually describing the key"""
		pass

	@staticmethod
	@abstractmethod
	def getNameOfCipher(key=None):
		"""Returns the name of the cipher.  If the key is provided, it will try to be more specific"""
		pass
