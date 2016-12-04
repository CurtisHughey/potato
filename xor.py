#!/usr/bin/env python3

from abc import abstractmethod
import utils
import cipher
import unittest
import stream

class Xor(stream.Stream):

	def encrypt(self, plaintext, key):
		state = self.initState(key)
		return super().applyPrf(plaintext, state)

	def decrypt(self, ciphertext, key):
		return self.encrypt(ciphertext, key)  # Symmetric

	def initState(self, seed):
		return seed  # Seed should just be the byte being xor'd with

	def prf(self, state):
		return (state, state)  # returning the byte as the first arg, state as the second arg

	def genKeys(self):
		return range(256)

	def crack(self, ciphertext):
		return super().bruteForce(ciphertext)  # can I define this method at higher level?...

	def getNameOfCipher(self):
		return "XOR (Stream)"

	def usage(self):
		print('Key should be number 0-255')

class XorTest(unittest.TestCase):

	def setUp(self):
		self.xorInstance = Xor()

	def test_encrypt(self):
		plaintext = '\x41\x42\x43'
		ciphertext = '\x00\x03\x02'

		self.assertEqual(self.xorInstance.encrypt(plaintext, 0x41), ciphertext)

	def test_decrypt(self):
		plaintext = '\x41\x42\x43'
		ciphertext = '\x00\x03\x02'

		self.assertEqual(self.xorInstance.decrypt(ciphertext, 0x41), plaintext)

	def test_identity(self):
		plaintext = '\x41\x42\x43'
		ciphertext = '\x00\x03\x02'

		self.assertEqual(self.xorInstance.decrypt(self.xorInstance.encrypt(plaintext, 0x41), 0x41), plaintext)
