#!/usr/bin/env python3

import utils
import cipher
import unittest

class Nothing(cipher.AbstractCipher):

	def encrypt(self, plaintext, key):
		return plaintext

	def decrypt(self, ciphertext, key):
		return ciphertext	

	def crack(self, ciphertext):
		chi2 = utils.calcChiSquared(ciphertext)

		return (None, chi2)

	def getNameOfCipher(self, key=None):
		return 'Nothing'

	def usage(self):
		print('Key is ignored.  Sees if plaintext')


class NothingTest(unittest.TestCase):

	def setUp(self):
		self.nothingInstance = Nothing()

	def test_encrypt(self):
		self.assertEqual(self.nothingInstance.encrypt('abc', (1,1)), 'abc')

	def test_decrypt(self):
		self.assertEqual(self.nothingInstance.decrypt('abc', (1,1)), 'abc')
