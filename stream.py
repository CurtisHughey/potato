#!/usr/bin/env python3

from abc import abstractmethod
import cipher

class Stream(cipher.AbstractBruteForceCipher):

	def applyPrf(self, plaintext, state):
		ciphertext = ''

		lowera = ord('a')
		for c in plaintext:
			(nextByte, state) = self.prf(state)
			ciphertext += chr(ord(c) ^ nextByte)

		return ciphertext

	@abstractmethod
	def initState(self, seed):
		"""Initializes the state of a PRF, returns it"""

	@abstractmethod
	def prf(self, state):
		"""Takes the current state and spits out a byte and the modified state"""

	# For these schemes, anything goes
	def onlyLowerCase(self):
		return False

